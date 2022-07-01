import json

import gidgethub.aiohttp
import pytest
import pytest_asyncio

from app.github.github_api import GithubAPI

GITHUB_USER_ID = "p0tato"
GITHUB_ACCESS_TOKEN = "some_access_token"


class TestClass:
    @staticmethod
    def _load_response(filename):
        with open(filename) as f:
            return json.loads(f.read())

    @pytest_asyncio.fixture
    async def gidgethub_instance(mock_http_client):
        return gidgethub.aiohttp.GitHubAPI(
            mock_http_client.session,
            requester=GITHUB_USER_ID,
            oauth_token=GITHUB_ACCESS_TOKEN,
        )

    @pytest_asyncio.fixture
    async def github_api(gidgethub_instance):
        return GithubAPI(gidgethub_instance, GITHUB_USER_ID)

    @property
    def org_membership_response(self):
        return self._load_response("tests/data/github/org_memberships_response.json")

    async def test_display_user(self, github_api: GithubAPI):
        assert github_api.username == GITHUB_USER_ID
