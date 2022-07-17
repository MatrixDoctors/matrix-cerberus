from unittest import mock

import gidgethub.aiohttp
import pytest
from aioresponses import aioresponses
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.core.http_client import http_client

GITHUB_USER_ID = "p0tato"
GITHUB_ACCESS_TOKEN = "some_access_token"


@pytest.fixture
def settings():
    return Settings.from_yaml("config.sample.yml")


@pytest.fixture
@mock.patch("app.core.config.settings", Settings.from_yaml("config.sample.yml"))
def client():
    from app.main import app

    return TestClient(app)


@pytest.fixture
def mock_server():
    with aioresponses() as m:
        yield m


@pytest.fixture
async def mock_http_client():
    await http_client.start_session()
    yield http_client


@pytest.fixture
async def gidgethub_instance(mock_http_client):
    return gidgethub.aiohttp.GitHubAPI(
        mock_http_client.session,
        requester=GITHUB_USER_ID,
        oauth_token=GITHUB_ACCESS_TOKEN,
    )


@pytest.fixture
@mock.patch("app.core.config.settings", Settings.from_yaml("config.sample.yml"))
async def github_api(gidgethub_instance):
    from app.github.github_api import GithubAPI

    return GithubAPI(gidgethub_instance, GITHUB_USER_ID)
