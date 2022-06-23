import random
import string

from app.core.background_runner import matrix_bot_runner
from app.core.models import RoomSpecificExternalUrl


class ExternalUrlAPI:
    """
    ExternalUrlAPI class which abstracts out the interactions between the Bot Client and the API routes.
    """

    def __init__(self):
        self._characters = string.ascii_letters + string.digits
        self._event_type = "matrix-cerberus.external_url"

    def _generate_url_code(self, N: int = 8):
        return "".join(random.choices(self._characters, k=N))

    def add_url_to_rooms(
        self, room_id: str, use_once_only: str, new_url_code: str, old_url_code: str = None
    ):
        """
        Method to add or replace url codes in a room.

        Parameters:
        'use_once_only` determines if the new_url_code is permanent or single-use.
        """
        if room_id not in matrix_bot_runner.client.room_to_external_url_mapping:
            matrix_bot_runner.client.room_to_external_url_mapping[
                room_id
            ] = RoomSpecificExternalUrl()

        room_specific_data = matrix_bot_runner.client.room_to_external_url_mapping[room_id]

        # If old_url_code is supplied then remove old_url_code and add new_url_code
        # Otherwise just add new_url_code to the Set.
        if use_once_only:
            room_specific_data.temporary.add(new_url_code)

            if old_url_code is not None:
                room_specific_data.temporary.remove(old_url_code)
        else:
            room_specific_data.permanent = new_url_code

    async def generate_url(self, room_id: str, use_once_only: bool):
        """
        Method to generate a new external url invite.
        """
        data = await matrix_bot_runner.client.get_account_data(self._event_type)
        external_url_data = data.content

        url_code = self._generate_url_code()
        while url_code in external_url_data:
            url_code = self._generate_url_code()

        external_url_data[url_code] = {"room_id": room_id, "use_once_only": use_once_only}
        data.content = external_url_data

        self.add_url_to_rooms(room_id, use_once_only, new_url_code=url_code)

        await matrix_bot_runner.client.put_account_data(self._event_type, data)
        return url_code

    async def get_room_invite(self, url_code: str, user_id: str):
        """
        Method to invite users to a room based on an existing external url invite code.
        """
        data = await matrix_bot_runner.client.get_account_data(self._event_type)
        external_url_data = data.content

        if url_code not in external_url_data:
            return False

        room_url_object = external_url_data[url_code]

        await matrix_bot_runner.client.room_invite(room_url_object.room_id, user_id)

        if room_url_object.use_once_only:
            matrix_bot_runner.client.room_to_external_url_mapping[
                room_url_object.room_id
            ].temporary.remove(url_code)
            del external_url_data[url_code]

        data.content = external_url_data
        await matrix_bot_runner.client.put_account_data(self._event_type, data)

        return True

    async def replace_existing_url(self, url_code: str):
        """
        This method replaces the supplied url code with a new url code and updates
        the '<app_name>.external_url` account data event and rooom to externalu url mapping object to match the same.

        'url_code' is assumed to be always valid i.e. exists in the respective account data events.
        """
        data = await matrix_bot_runner.client.get_account_data(self._event_type)
        external_url_data = data.content
        room_url_object = external_url_data[url_code]

        # Generate new url and use the old data
        new_url_code = self._generate_url_code()
        while new_url_code in external_url_data:
            new_url_code = self._generate_url_code()

        external_url_data[new_url_code] = {
            "room_id": room_url_object.room_id,
            "use_once_only": room_url_object.use_once_only,
        }

        self.add_url_to_rooms(
            room_url_object.room_id,
            room_url_object.use_once_only,
            new_url_code=new_url_code,
            old_url_code=url_code,
        )
        del external_url_data[url_code]

        data.content = external_url_data
        await matrix_bot_runner.client.put_account_data(self._event_type, data)

        return new_url_code
