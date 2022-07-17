import asyncio
from typing import Set, Dict, List

import gidgethub.aiohttp
from nio import ErrorResponse, RoomGetStateEventError, RoomInviteError, RoomKickError

from app.core.app_state import app_state
from app.core.models import RoomSpecificData, UserData
from app.github.github_api import GithubAPI


class RegisteredUser:
    def __init__(self, user_data: UserData):
        self.github_username = user_data.content.github.username

        if self.github_username is not None:
            gh = gidgethub.aiohttp.GitHubAPI(
                app_state.http_client.session,
                requester=self.github_username,
                oauth_token=user_data.content.github.access_token,
            )

            self.github_api = GithubAPI(
                gh=gh,
                username=self.github_username,
                default_role=app_state.settings.github.organisation_membership,
            )


class BackgroundValidater:
    def __init__(self):
        self.client = app_state.bot_client
        self.registered_users: Dict[str, RegisteredUser] = dict()

        # List of rooms registered under the application and has "room membership" conditions.
        self.rooms_with_conditions: List[str] = []

        # Set of rooms where the bot has invite and kick permissions.
        self.rooms_with_permissions: Set[str] = {}
        self.background_validator_task = None

    async def create_background_task(self):
        print("Background validator has started")
        self.background_validator_task = asyncio.create_task(self.start_task())

    async def cancel_background_task(self):
        self.background_validator_task.cancel()
        print("Background validator has stopped")

    async def start_task(self):
        while True:
            await self.fetch_rooms_and_users()

            for room_id in self.rooms_with_conditions:
                # When the bot is either not part of the room or dosen't have the required permissions.
                if room_id not in self.rooms_with_permissions or room_id not in self.client.rooms:
                    continue

                ignore_members = await self.get_users_not_removed_by_bot(room_id)
                room_specific_data = await self.client.get_account_data("rooms", room_id=room_id)

                for user_id in self.registered_users.keys():
                    if user_id in ignore_members:
                        continue

                    current_state = await self.get_current_room_membership(user_id, room_id)
                    if current_state == "ignore":
                        continue
                    print(user_id, current_state)

                    is_permitted_through_github = await self.check_github_conditions(
                        user_id, room_specific_data
                    )
                    is_permitted = is_permitted_through_github

                    next_state = await self.decide_next_state_of_user(
                        current_state, is_permitted, room_specific_data.content.disable_room_kick
                    )

                    if current_state == next_state:
                        continue

                    await self.send_next_state_event(room_id, user_id, next_state)

                await asyncio.sleep(1)
            await asyncio.sleep(1)

    async def fetch_rooms_and_users(self):
        resp = await self.client.get_account_data("global_data")
        self.rooms_with_conditions = resp.content.rooms

        for user_id in resp.content.users:
            user_data = await self.client.get_account_data("user", user_id=user_id)
            self.registered_users[user_id] = RegisteredUser(user_data)

        self.rooms_with_permissions = await self.client.get_rooms_with_mod_permissions(
            self.client.user_id
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
        Method which validates a user's room membership based on a list of github conditions set by the room admin.
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

            # Repository conditions
            for repo_name, repo_conditions in org_conditions.repos.items():
                resp = await gh_api.repo_permissions(org_name, repo_name, gh_username)

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
            if sponsoring_tier and org_conditions.sponsorship_tiers[sponsoring_tier]:
                return True

        # Organisation conditions
        for user_name, user_conditions in room_github_conditions.users.items():

            # Repository conditions
            for repo_name, repo_conditions in user_conditions.repos.items():
                resp = await gh_api.repo_permissions(user_name, repo_name, gh_username)

                if resp == "admin" and repo_conditions.admin:
                    return True
                elif resp == "write" and repo_conditions.write:
                    return True
                elif resp == "read" and repo_conditions.read:
                    return True

            # Sponsorship tier conditions
            sponsoring_tier = await gh_api.user_sponsored_at_tier(user_name)
            if sponsoring_tier and user_conditions.sponsorship_tiers[sponsoring_tier]:
                return True

        return False

    async def decide_next_state_of_user(
        self, current_state: str, is_permitted: bool, disable_room_kick: str
    ) -> str:
        """
        Returns the next state of the user (str).
        """

        if is_permitted:
            if current_state == "join":
                return current_state
            else:
                return "invite"
        elif disable_room_kick:
            return current_state
        else:
            return "leave"

    async def send_next_state_event(self, room_id: str, user_id: str, next_state: str):
        """
        Sends a state event which sets the room membership for a user.
        """

        if next_state == "invite":
            resp = await self.client.room_invite(room_id, user_id)

            if isinstance(resp, RoomInviteError):
                print(f"Error: {resp}")

        elif next_state == "leave":
            resp = await self.client.room_kick(room_id, user_id)

            if isinstance(resp, RoomKickError):
                print(f"Error: {resp}")

    async def get_users_not_removed_by_bot(self, room_id: str) -> Set[str]:
        """
        Method that returns the set of users whose 'leave' state is not a result of the bot's actions.
        """

        ignore_members = set()

        resp = await self.client.get_room_members(room_id)
        if isinstance(resp, ErrorResponse):
            print(f"Error: {resp}")

        for room_member in resp.chunk:
            # Bot is not the event's sender.
            if room_member.sender != self.client.user_id:
                ignore_members.add(room_member.state_key)

        return ignore_members


background_validator = BackgroundValidater()
