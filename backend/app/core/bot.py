import asyncio
import json
import os
import sys
from asyncio import exceptions
from typing import Optional

from nio import (
    AsyncClient,
    AsyncClientConfig,
    InviteEvent,
    LoginResponse,
    MatrixRoom,
    RoomMessageText,
)

from app.core.config import settings


class BaseBotClient(AsyncClient):
    def __init__(
        self,
        homeserver: str,
        user: str = "",
        device_id: Optional[str] = "",
        store_path: Optional[str] = "",
        config: Optional[AsyncClientConfig] = None,
        ssl: Optional[bool] = None,
        proxy: Optional[str] = None,
    ):
        super().__init__(homeserver, user, device_id, store_path, config, ssl, proxy)

        self.password = None

        # auto-join room invites
        self.add_event_callback(self.cb_autojoin_room, InviteEvent)

        # print all the messages we receive
        self.add_event_callback(self.cb_print_messages, RoomMessageText)

    async def login(self) -> None:
        # Log in either using the session details file or the username, password (if the file dosen't exist)
        if os.path.exists(settings.matrix_bot.session_details_file) and os.path.isfile(
            settings.matrix_bot.session_details_file
        ):
            try:
                with open(settings.matrix_bot.session_details_file, "r") as f:
                    config = json.load(f)
                    self.access_token = config["access_token"]
                    self.user_id = config["user_id"]
                    self.device_id = config["device_id"]

            except IOError as err:
                print(f"Couldn't load session from file. Logging in. Error: {err}")
            except json.JSONDecodeError:
                print("Couldn't read JSON file; overwriting")

        # If the previous session is not stored, we'll log in with a password
        if not self.user_id or not self.access_token or not self.device_id:
            if self.password is None:
                print("Password is blank")
                sys.exit(1)

            resp = await super().login(self.password, device_name=self.device_id)

            if isinstance(resp, LoginResponse):
                self.__write_details_to_disk(resp)
            else:
                print(f"Failed to log in: {resp}")
                sys.exit(1)

    async def cb_autojoin_room(self, room: MatrixRoom, event: InviteEvent):
        # Callback to automatically join a Matrix room on invite.
        await self.join(room.room_id)

    async def cb_print_messages(self, room: MatrixRoom, event: RoomMessageText):
        # Callback to print all received messages to stdout.
        print(f"{room.display_name} @{room.user_name(event.sender)}: {event.body}")

    async def send_message_to_room(self, room_id, msg):
        try:
            await self.room_send(
                room_id=room_id,
                message_type="m.room.message",
                content={
                    "msgtype": "m.text",
                    "body": f"{msg}",
                },
            )
        except exceptions as err:
            print(err)

    @staticmethod
    def __write_details_to_disk(resp: LoginResponse) -> None:
        """Writes login details to disk so that we can restore our session later
        without logging in again and creating a new device ID.
        """
        with open(settings.matrix_bot.session_details_file, "w") as f:
            json.dump(
                {
                    "access_token": resp.access_token,
                    "device_id": resp.device_id,
                    "user_id": resp.user_id,
                },
                f,
            )

    @classmethod
    def get_bot_client(cls):
        client = BaseBotClient(
            settings.matrix_bot.homeserver,
            settings.matrix_bot.user_id,
            device_id=settings.matrix_bot.device_id,
        )
        client.password = settings.matrix_bot.password

        return client
