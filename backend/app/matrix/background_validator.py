import asyncio

from nio import RoomGetStateEventError

from app.core.app_state import app_state


class BackgroundValidater:
    def __init__(self):
        self.client = app_state.bot_client
        self.registered_users = []
        self.rooms_with_conditions = []
        self.rooms_with_permissions = {}
        self.background_validator_task = None

    async def create_background_task(self):
        print("Background validator has started")
        self.background_validator_task = asyncio.create_task(self.start_task())

    async def cancel_background_task(self):
        self.background_validator_task.cancel()
        print("Background validator has stopped")

    async def start_task(self):
        while True:
            print("running")
            resp = await self.client.get_account_data("global_data")
            self.rooms_with_conditions = resp.content.rooms
            self.registered_users = resp.content.users

            self.rooms_with_permissions = await self.client.get_rooms_with_mod_permissions(
                self.client.user_id
            )

            for user_id in self.registered_users:
                for room_id in self.rooms_with_conditions:
                    if room_id not in self.rooms_with_permissions:
                        continue

                    membership = await self.get_current_room_membership(user_id, room_id)
                    if membership == "ignore":
                        continue
                    print(user_id, membership)

                await asyncio.sleep(1)
            await asyncio.sleep(1)

    async def get_current_room_membership(self, user_id: str, room_id: str):
        matrix_room_object = self.client.rooms[room_id]

        if user_id in matrix_room_object.users:
            if matrix_room_object.users[user_id].invited:
                return "invite"
            else:
                return "join"
        else:
            # how to raise error when 403
            resp = await self.client.room_get_state_event(
                room_id=room_id, event_type="m.room.member", state_key=user_id
            )

            if isinstance(resp, RoomGetStateEventError):
                return "ignore"

            membership = resp.content["membership"]
            if membership == "leave" or membership == "ban":
                return "ignore"
            elif membership == "knock":
                return "knock"


background_validator = BackgroundValidater()
