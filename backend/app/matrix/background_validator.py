import asyncio
from typing import Set, Dict

import gidgethub.aiohttp
from loguru import logger
from nio import ErrorResponse, RoomGetStateEventError, RoomInviteError, RoomKickError

from app.core.bot import BaseBotClient
from app.core.http_client import HttpClient
from app.core.models import RoomSpecificData, UserData
from app.github.github_api import GithubAPI
from app.patreon.patreon_api import PatreonAPI


class RegisteredUser:
    def __init__(self, user_data: UserData, http_client: HttpClient, default_role: str):
        self.github_username = user_data.content.github.username
        self.patreon_username = user_data.content.patreon.email

        if self.github_username is not None:
            gh = gidgethub.aiohttp.GitHubAPI(
                http_client.session,
                requester=self.github_username,
                oauth_token=user_data.content.github.access_token,
            )

            self.github_api = GithubAPI(
                gh=gh,
                username=self.github_username,
                default_role=default_role,
            )

        if self.patreon_username is not None:
            self.patreon_api = PatreonAPI(
                email=self.patreon_username,
                access_token=user_data.content.patreon.access_token,
                session=http_client.session,
            )


class RegisteredRoom:
    def __init__(self, room_data: RoomSpecificData, ignored_users: Set[str]):
        self.room_data = room_data
        self.ignored_users = ignored_users


class BackgroundValidater:
    def __init__(
        self,
        bot_client: BaseBotClient,
        http_client: HttpClient,
        github_default_role: str,
        bg_validation_cooldown: int,
    ):
        self.client = bot_client
        self.http_client = http_client
        self.github_default_role = github_default_role
        self.bg_validation_cooldown = bg_validation_cooldown

        self.registered_users: Dict[str, RegisteredUser] = dict()

        self.github_id_to_matrix_id = dict()

        # List of rooms registered under the application and has "room membership" conditions.
        self.rooms_with_conditions: Dict[str, RegisteredRoom] = dict()

        # Set of rooms where the bot has invite and kick permissions.
        self.rooms_with_mod_permissions: Set[str] = set()

        # Queue to keep track of rooms whose permissions are recently modified.
        self.queue = asyncio.Queue()

        self.background_validator_task = None

        self.queue_processor_task = None

    async def create_background_task(self):
        logger.success("Background validator has started")
        self.background_validator_task = asyncio.create_task(self.start_task())
        self.queue_processor_task = asyncio.create_task(self.process_queue())

    async def cancel_background_task(self):
        self.background_validator_task.cancel()
        self.queue_processor_task.cancel()
        logger.success("Background validator has stopped")

    @logger.catch
    async def main_task(self):
        """
        The main background validator task which validates the room memberships of registered users for all the rooms with conditions.
        """
        while True:
            await self.fetch_rooms_and_users()

            for room_id in self.rooms_with_conditions.keys():
                for user_id in self.registered_users.keys():
                    await self.validate_room_membership_of_user(room_id, user_id)
            await asyncio.sleep(self.bg_validation_cooldown)

    async def process_queue(self):
        """
        Method which validates room memberships for all recently modified rooms in the queue.
        """
        while True:

            # Blocks until the queue is not empty
            type, id = await self.queue.get()
            if type == "room":
                room_specific_data = await self.client.get_account_data(type="rooms", room_id=id)
                ignored_users = await self.get_ignored_users_for_a_room(id)
                self.rooms_with_conditions[id] = RegisteredRoom(
                    room_data=room_specific_data, ignored_users=ignored_users
                )

                for user_id in self.registered_users.keys():
                    await self.validate_room_membership_of_user(room_id=id, user_id=user_id)

            elif type == "user":
                user_data = await self.client.get_account_data("user", user_id=id)
                self.registered_users[id] = RegisteredUser(
                    user_data=user_data,
                    http_client=self.http_client,
                    default_role=self.github_default_role,
                )

                for room_id in self.rooms_with_conditions.keys():
                    await self.validate_room_membership_of_user(room_id=room_id, user_id=id)

    async def add_room_to_queue(self, room_id: str):
        await self.queue.put(["room", room_id])

    async def add_user_to_queue(self, user_id: str):
        await self.queue.put(["user", user_id])

    async def validate_room_membership_of_user(self, room_id: str, user_id: str):
        ignore_members = self.rooms_with_conditions[room_id].ignored_users
        room_specific_data = self.rooms_with_conditions[room_id].room_data

        if user_id in ignore_members:
            return

        current_state = await self.get_current_room_membership(user_id, room_id)

        # Avoid checking the conditions if the user is to be ignored
        # or the user is already part of the room or invited and the room has disabled bot kicks.
        if current_state == "ignore":
            return

        if room_specific_data.content.disable_room_kick:
            if current_state == "join" or current_state == "invite":
                return

        is_permitted_through_github = await self.check_github_conditions(
            user_id, room_specific_data
        )
        is_permitted = is_permitted_through_github
        print(is_permitted, user_id)

        next_state = await self.decide_next_state_of_user(current_state, is_permitted)

        if current_state == next_state:
            return

        await self.send_next_state_event(room_id, user_id, next_state)

    async def fetch_rooms_and_users(self):
        """
        Fetch the list of all registered users and rooms with conditions.

        Update the room list if any room doesn't satisfy the following conditions:
            1) Bot is not a member of the room
            2) Bot doesn't have necessary permissions to invite and kick.
        """
        resp = await self.client.get_account_data("global_data")

        # User Data

        for user_id in resp.content.users:
            user_data = await self.client.get_account_data("user", user_id=user_id)
            self.registered_users[user_id] = RegisteredUser(
                user_data=user_data,
                http_client=self.http_client,
                default_role=self.github_default_role,
            )

            # Cache the mapping between github id and matrix id
            self.github_id_to_matrix_id[user_data.content.github.username] = user_id

        # Room Data

        self.rooms_with_mod_permissions = await self.client.get_rooms_with_mod_permissions(
            self.client.user_id
        )

        # Remove rooms where the bot is not a member/dosen't have kick and invite permissions
        rooms_to_be_removed = set()
        for room_id in resp.content.rooms:
            if room_id not in self.rooms_with_mod_permissions:
                # Remove room data from cache
                if room_id in self.rooms_with_conditions:
                    del self.rooms_with_conditions[room_id]

                # Remove room data from bot state
                await self.client.put_account_data(type="rooms", data={}, room_id=room_id)
                rooms_to_be_removed.add(room_id)

        # Update room list in bot state
        if len(rooms_to_be_removed) > 0:
            filtered_rooms = set(resp.content.rooms) - rooms_to_be_removed
            resp.content.rooms = list(filtered_rooms)
            await self.client.put_account_data(type="global_data", data=resp)

        # Cache all room conditions
        for room_id in resp.content.rooms:
            room_specific_data = await self.client.get_account_data(type="rooms", room_id=room_id)
            ignored_users = await self.get_ignored_users_for_a_room(room_id)
            self.rooms_with_conditions[room_id] = RegisteredRoom(
                room_data=room_specific_data, ignored_users=ignored_users
            )

    async def get_current_room_membership(self, user_id: str, room_id: str) -> str:
        matrix_room_object = self.client.rooms[room_id]

        if user_id in matrix_room_object.users:
            if matrix_room_object.users[user_id].invited:
                return "invite"
            else:
                return "join"
        else:
            resp = await self.client.room_get_state_event(
                room_id=room_id, event_type="m.room.member", state_key=user_id
            )

            if isinstance(resp, RoomGetStateEventError):
                return "ignore"

            membership = resp.content["membership"]

            if membership == "ban":
                return "ignore"
            return membership

    async def check_github_conditions(
        self, user_id: str, room_specific_data: RoomSpecificData
    ) -> bool:
        """
        Method to validate a user's room membership based on a list of github conditions set by the room admin.
        """

        room_github_conditions = room_specific_data.content.github

        # If there are no conditions present
        if len(room_github_conditions.orgs) == 0 and len(room_github_conditions.users) == 0:
            return True

        # If the user didn't register with github.
        if self.registered_users[user_id].github_username is None:
            return False

        gh_username = self.registered_users[user_id].github_username
        gh_api = self.registered_users[user_id].github_api

        # Organisation conditions
        for org_name, org_conditions in room_github_conditions.orgs.items():

            # Using access token of the admin who last edited the github condition.
            admin_matrix_id = org_conditions.last_edited_by
            admin_gh_api = self.registered_users[admin_matrix_id].github_api

            # Repository conditions
            for repo_name, repo_conditions in org_conditions.repos.items():
                resp = await admin_gh_api.repo_permissions(org_name, repo_name, gh_username)

                if resp == "admin" and repo_conditions.admin:
                    return True
                elif resp == "write" and repo_conditions.write:
                    return True
                elif resp == "read" and repo_conditions.read:
                    return True

            # Team conditions
            for team_name, is_team_allowed in org_conditions.teams.items():
                resp = await gh_api.is_team_member(org_name, team_name, gh_username)

                if resp and is_team_allowed:
                    return True

            # Sponsorship tier conditions
            sponsoring_tier = await gh_api.org_sponsored_at_tier(org_name)
            if (
                sponsoring_tier
                and org_conditions.sponsorship_tiers
                and org_conditions.sponsorship_tiers[sponsoring_tier]
            ):
                return True

        # User conditions
        for user_name, user_conditions in room_github_conditions.users.items():
            # Using access token of the owner
            owner_matrix_id = self.github_id_to_matrix_id[user_name]
            owner_gh_api = self.registered_users[owner_matrix_id].github_api

            # Repository conditions
            for repo_name, repo_conditions in user_conditions.repos.items():
                resp = await owner_gh_api.repo_permissions(user_name, repo_name, gh_username)

                if resp == "admin" and repo_conditions.admin:
                    return True
                elif resp == "write" and repo_conditions.write:
                    return True
                elif resp == "read" and repo_conditions.read:
                    return True

            # Sponsorship tier conditions
            sponsoring_tier = await gh_api.user_sponsored_at_tier(user_name)
            if (
                sponsoring_tier
                and user_conditions.sponsorship_tiers
                and user_conditions.sponsorship_tiers[sponsoring_tier]
            ):
                return True

        return False

    async def check_patreon_conditions(
        self, user_id: str, room_specific_data: RoomSpecificData
    ) -> bool:
        """
        Method which validates a user's room membership based on a list of patreon campaign conditions set by the room admin.
        """
        campaign_conditions = room_specific_data.content.patreon.campaigns

        # If there are no conditions present
        if len(campaign_conditions) == 0:
            return True

        # If the user didn't register with patreon.
        if self.registered_users[user_id].patreon_username is None:
            return False

        patreon_api = self.registered_users[user_id].patreon_api

        memerships_list = await patreon_api.user_memberships()

        for member_id in memerships_list:
            membership_data = await patreon_api.membership_details(member_id)
            campaign_id = membership_data["campaign_id"]

            if campaign_id in campaign_conditions:
                for tier_id in membership_data["tiers"]:
                    if (
                        tier_id in campaign_conditions[campaign_id].tiers
                        and campaign_conditions[campaign_id].tiers[tier_id].is_enabled
                    ):
                        return True

        return False

    async def decide_next_state_of_user(self, current_state: str, is_permitted: bool) -> str:
        """
        Returns the next state of the user (str).
        """

        if is_permitted:
            if current_state == "join":
                return current_state
            else:
                return "invite"
        else:
            return "leave"

    async def send_next_state_event(self, room_id: str, user_id: str, next_state: str):
        """
        Sends a state event which sets the room membership for a user.
        """

        if next_state == "invite":
            resp = await self.client.room_invite(room_id, user_id)

            if isinstance(resp, RoomInviteError):
                logger.error(f"Error: {resp}")

        elif next_state == "leave":
            resp = await self.client.room_kick(room_id, user_id)

            if isinstance(resp, RoomKickError):
                logger.error(f"Error: {resp}")

    async def get_ignored_users_for_a_room(self, room_id: str) -> Set[str]:
        """
        Method that returns the set of users to ignore.
        """

        ignore_members = set()

        # Users whose power level exceeds the bot's current power level.
        power_levels = self.client.rooms[room_id].power_levels
        for room_member_id in self.registered_users.keys():
            if power_levels.get_user_level(room_member_id) >= power_levels.get_user_level(
                self.client.user_id
            ):
                ignore_members.add(room_member_id)

        # Set of users whose 'leave' state is not a result of the bot's actions.
        resp = await self.client.get_room_members(room_id)
        if isinstance(resp, ErrorResponse):
            logger.error(f"Error: {resp}")

        for room_member in resp.chunk:
            # Bot is not the event's sender.
            if room_member.sender != self.client.user_id:
                ignore_members.add(room_member.state_key)

        return ignore_members
