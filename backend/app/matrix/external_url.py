import random
import string

from app.core.background_runner import matrix_bot_runner


class ExternalUrl:
    """
    ExternalUrl class which abstracts out the interactions between the Bot Client and the API routes.
    """

    def __init__(self):
        self._characters = string.ascii_letters + string.digits

    def _generate_url_code(self, N: int = 8):
        return "".join(random.choices(self._characters, k=N))

    async def generate_url(self, matrix_homeserver: str, room_id: str, use_once_only: bool):
        data = await matrix_bot_runner.client.get_account_data(
            "matrix-cerberus.external_url", matrix_homeserver
        )
        external_url_data = data.content

        url_code = self._generate_url_code()
        while url_code in external_url_data:
            url_code = self._generate_url_code()

        external_url_data[url_code] = {"room_id": room_id, "use_once_only": use_once_only}

        data = {"content": external_url_data}

        await matrix_bot_runner.client.put_account_data(
            "matrix-cerberus.external_url", matrix_homeserver, data
        )
        return url_code
