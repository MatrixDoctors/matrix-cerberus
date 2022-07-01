import json

import pytest
from aioresponses import aioresponses
from fastapi.testclient import TestClient
from nio import AsyncClient, LoginResponse

from app.core.background_runner import matrix_bot_runner
from app.main import app
from app.matrix.external_url import ExternalUrlAPI

TEST_USER_ID = "@example:matrix.org"
TEST_DEVICE_ID = "GHTYAJCE"

client = TestClient(app)


class TestClass:
    @pytest.fixture
    async def external_url_api(self):
        return ExternalUrlAPI()

    @pytest.fixture
    def mock_server(self):
        with aioresponses() as m:
            yield m

    @staticmethod
    def _load_response(filename):
        with open(filename) as f:
            return json.loads(f.read())

    @property
    def login_response(self):
        return self._load_response("tests/data/login_response.json")

    @pytest.fixture
    async def async_client(self):
        client = AsyncClient("https://matrix.org")
        yield client

        await client.close()

    @pytest.mark.asyncio
    async def test_whoami(self, async_client, mock_server):
        await async_client.receive_response(LoginResponse.from_dict(self.login_response))
        assert async_client.logged_in

        mock_server.get(
            url="https://matrix.org/_matrix/client/r0/account/whoami?access_token=some_access_token",
            status=200,
            payload={"device_id": TEST_DEVICE_ID, "user_id": TEST_USER_ID},
        )

        resp = await async_client.whoami()
        assert resp.user_id == TEST_USER_ID

        assert async_client.access_token == "some_access_token"
        assert async_client.user_id == TEST_USER_ID
