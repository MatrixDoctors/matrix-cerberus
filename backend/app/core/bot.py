import sys
from asyncio import exceptions
from typing import Optional

from nio import AsyncClient, AsyncClientConfig, InviteEvent, MatrixRoom, RoomMessageText
from nio.responses import WhoamiResponse

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

        # auto-join room invites
        self.add_event_callback(self.cb_autojoin_room, InviteEvent)

        # print all the messages we receive to console
        self.add_event_callback(self.cb_print_messages, RoomMessageText)

    async def login(self) -> None:
        self.access_token = settings.matrix_bot.access_token

        # Verify the access_token and set user_id
        response = await self.whoami()

        if isinstance(response, WhoamiResponse):
            self.user_id = response.user_id
        else:
            raise ValueError(f"Failed to log in: Access token or homeserver is invalid")

    async def cb_autojoin_room(self, room: MatrixRoom, event: InviteEvent):
        await self.join(room.room_id)

    async def cb_print_messages(self, room: MatrixRoom, event: RoomMessageText):
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
