"""
Module which provides classes and methods that interact with a matrix homeserver as a bot client.
"""

from typing import Optional
from asyncio import exceptions
from urllib.parse import urljoin

from nio import AsyncClient, AsyncClientConfig, InviteEvent, MatrixRoom, RoomMessageText
from nio.responses import WhoamiResponse

from app.core.http_client import http_client
from app.core.models import (
    BotGlobalData,
    ExternalUrlData,
    RoomSpecificData,
    RoomSpecificExternalUrl,
    UserData,
)


class BaseBotClient(AsyncClient):
    def __init__(
        self,
        homeserver: str,
        app_name: str,
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

        self.room_to_external_url_mapping = {}

        self.app_name = app_name

    async def login(self, access_token) -> None:
        self.access_token = access_token

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

    def parse_event_data(self, type: str, data):
        if type == f"external_url":
            return ExternalUrlData.parse_obj(data)

        elif type == "rooms":
            return RoomSpecificData.parse_obj(data)

        elif type == "user":
            return UserData.parse_obj(data)

        elif type == "global_data":
            return BotGlobalData.parse_obj(data)

    def parse_event_type(self, type: str, app_name, **additional_type_data):
        if type == f"external_url":
            event_type = f"{app_name}.external_url"

        elif type == "rooms":
            event_type = f"{app_name}.rooms.{additional_type_data['room_id']}"

        elif type == "user":
            event_type = f"{app_name}.user.{additional_type_data['user_id']}"

        elif type == "global_data":
            event_type = f"{app_name}.global_data"

        return event_type

    async def get_account_data(self, type: str, **additional_type_data):
        access_token = self.access_token
        headers = {"Authorization": f"Bearer {access_token}"}
        event_type = self.parse_event_type(type, self.app_name, **additional_type_data)

        url = urljoin(
            self.homeserver, f"/_matrix/client/v3/user/{self.user_id}/account_data/{event_type}"
        )

        async with http_client.session.get(url=url, headers=headers) as resp:
            data = await resp.json()
            data = self.parse_event_data(type, data)
            return data

    async def put_account_data(self, type: str, data, **additional_type_data):
        access_token = self.access_token
        headers = {"Authorization": f"Bearer {access_token}"}

        event_type = self.parse_event_type(type, self.app_name, **additional_type_data)
        data = self.parse_event_data(type, data)

        url = urljoin(
            self.homeserver, f"/_matrix/client/v3/user/{self.user_id}/account_data/{event_type}"
        )
        await http_client.session.put(url=url, headers=headers, data=data.json())

    async def create_room_to_external_url_mapping(self):
        data = await self.get_account_data("external_url")
        external_url_data = data.content

        for url_code, value in external_url_data.items():
            if value.room_id not in self.room_to_external_url_mapping:
                self.room_to_external_url_mapping[value.room_id] = RoomSpecificExternalUrl()

            if value.use_once_only:
                self.room_to_external_url_mapping[value.room_id].temporary.add(url_code)
            else:
                self.room_to_external_url_mapping[value.room_id].permanent = url_code

    async def get_rooms_with_mod_permissions(self, user_id: str):
        rooms_with_mod_permissions = {}
        for room_id, room_object in self.rooms.items():
            # Check if bot has permissions to kick and invite
            if room_object.power_levels.can_user_invite(
                self.user_id
            ) and room_object.power_levels.can_user_kick(self.user_id):
                # Check if user is a member of the room
                if user_id in room_object.users and not room_object.users[user_id].invited:
                    if room_object.power_levels.get_user_level(user_id) >= 50:
                        rooms_with_mod_permissions[room_id] = room_object.named_room_name()
        return rooms_with_mod_permissions
