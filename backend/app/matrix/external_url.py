import random
import string

from app.core.background_runner import matrix_bot_runner


class ExternalUrl:
    """
    ExternalUrl class which abstracts out the interactions between the Bot Client and the API routes.
    """

    def __init__(self):
        self._characters = string.ascii_letters + string.digits
        self._event_type = "matrix-cerberus.external_url"

    def _generate_url_code(self, N: int = 8):
        return "".join(random.choices(self._characters, k=N))

    async def parse_data_and_save(self, matrix_homeserver, external_url_data):
        data = {"content": external_url_data}

        await matrix_bot_runner.client.put_account_data(self._event_type, matrix_homeserver, data)

    async def generate_url(self, matrix_homeserver: str, room_id: str, use_once_only: bool):
        data = await matrix_bot_runner.client.get_account_data(self._event_type, matrix_homeserver)
        external_url_data = data.content
        url_code = self._generate_url_code()
        while url_code in external_url_data:
            url_code = self._generate_url_code()

        external_url_data[url_code] = {"room_id": room_id, "use_once_only": use_once_only}

        await self.parse_data_and_save(matrix_homeserver, external_url_data)
        return url_code

    async def get_room_invite(self, matrix_homeserver: str, url_code: str, user_id: str):
        data = await matrix_bot_runner.client.get_account_data(self._event_type, matrix_homeserver)
        external_url_data = data.content

        if url_code not in external_url_data:
            return False

        await matrix_bot_runner.client.room_invite(external_url_data[url_code].room_id, user_id)

        if external_url_data[url_code].use_once_only:
            del external_url_data[url_code]

        await self.parse_data_and_save(matrix_homeserver, external_url_data)
        return True

    async def replace_existing_url(self, matrix_homeserver: str, url_code: str):
        data = await matrix_bot_runner.client.get_account_data(self._event_type, matrix_homeserver)
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

        del external_url_data[url_code]

        await self.parse_data_and_save(matrix_homeserver, external_url_data)

        return new_url_code
