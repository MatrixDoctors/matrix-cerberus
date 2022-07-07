import asyncio
from typing import Set, Dict, List

import gidgethub.aiohttp
from nio import ErrorResponse, RoomGetStateEventError
from pydantic import ValidationError

from app.core.app_state import app_state
from app.core.models import UserData
from app.github.github_api import GithubAPI


class RegisteredUser:
    def __init__(self, user_data: UserData):
        self.github_username = user_data.content.github.username

        gh = gidgethub.aiohttp.GitHubAPI(
            app_state.http_client.session,
            requester=self.github_username,
            oauth_token=user_data.content.github.access_token,
        )

        self.github_api = GithubAPI(gh=gh, username=self.github_username, default_role=app_state.settings.github.organisation_membership)


class BackgroundValidater:
    def __init__(self):
        self.client = app_state.bot_client
        self.registered_users: Dict[str, RegisteredUser] = dict()
        self.rooms_with_conditions: List[str] = []
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
                # When the user is either not part of the room or dosen't have the required permissions.
                if room_id not in self.rooms_with_permissions or room_id not in self.client.rooms:
                    continue

                ignore_members = await self.get_users_not_removed_by_bot(room_id)
                # room_specific_data = await self.client.get_account_data("rooms", room_id=room_id)

                for user_id, user_data in self.registered_users.items():
                    if user_id in ignore_members:
                        continue

                    membership = await self.get_current_room_membership(user_id, room_id)
                    if membership == "ignore":
                        continue
                    print(user_id, membership)

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

    async def check_github_conditions():
        pass

    async def get_users_not_removed_by_bot(self, room_id: str) -> Set[str]:
        """
        Method that returns the set of users whose 'leave' state is not a result of the bot's actions.
        """
        try:
            resp = await self.client.get_room_members(room_id)
            if isinstance(resp, ErrorResponse):
                print("Error: ", err, sep=" ")
        except ValidationError as err:
            print("Error: ", err, sep=" ")

        ignore_members = set()

        for room_member in resp.chunk:
            # Bot is not the event's sender.
            if room_member.sender != self.client.user_id:
                ignore_members.add(room_member.state_key)

        return ignore_members


background_validator = BackgroundValidater()
