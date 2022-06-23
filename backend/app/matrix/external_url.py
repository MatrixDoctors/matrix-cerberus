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

    async def generate_url(self, room_id: str, use_once_only: bool):
        """
        Method to generate a new external url invite.
        """
        data = await matrix_bot_runner.client.get_account_data(self._event_type)
        external_url_data = data.content
        print(data)

        url_code = self._generate_url_code()
        while url_code in external_url_data:
            url_code = self._generate_url_code()

        external_url_data[url_code] = {"room_id": room_id, "use_once_only": use_once_only}
        data.content = external_url_data

        await matrix_bot_runner.client.put_account_data(self._event_type, data)
        return url_code

    async def get_room_invite(self, url_code: str, user_id: str):
        """
        Method to invite users to a room based on an existing external url invite code.
        """
        data = await matrix_bot_runner.client.get_account_data(self._event_type)
        external_url_data = data.content
        print(data)

        if url_code not in external_url_data:
            return False

        room_url_object = external_url_data[url_code]

        await matrix_bot_runner.client.room_invite(room_url_object.room_id, user_id)

        if room_url_object.use_once_only:
            del external_url_data[url_code]

        data.content = external_url_data
        await matrix_bot_runner.client.put_account_data(self._event_type, data)

        return True

    async def replace_existing_url(self, url_code: str):
        """
        This method replaces the supplied url code with a new url code and updates
        the '<app_name>.external_url` and '<app_name>.rooms.<room_id>` account data events to match the same.

        'url_code' is assumed to be always valid i.e. exists in the respective account data events.
        """
        data = await matrix_bot_runner.client.get_account_data(self._event_type)
        external_url_data = data.content
        room_url_object = external_url_data[url_code]
        print(data)

        # Generate new url and use the old data
        new_url_code = self._generate_url_code()
        while new_url_code in external_url_data:
            new_url_code = self._generate_url_code()

        external_url_data[new_url_code] = {
            "room_id": room_url_object.room_id,
            "use_once_only": room_url_object.use_once_only,
        }

        del external_url_data[url_code]

        data.content = external_url_data
        await matrix_bot_runner.client.put_account_data(self._event_type, data)

        return new_url_code
