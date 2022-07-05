from unittest import mock

import gidgethub.aiohttp
import pytest
from aioresponses import aioresponses
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.core.http_client import http_client
from app.github.github_api import GithubAPI

GITHUB_USER_ID = "p0tato"
GITHUB_ACCESS_TOKEN = "some_access_token"


@pytest.fixture
def settings():
    return Settings.from_yaml("config.sample.yml")


@pytest.fixture
def app(mocker):
    mocker.patch("app.core.config.settings", Settings.from_yaml("config.sample.yml"))
    import app

    return app


@pytest.fixture
def client(mocker):
    mocker.patch("app.core.config.settings", Settings.from_yaml("config.sample.yml"))
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
    await http_client.stop_session()


@pytest.fixture
async def gidgethub_instance(mock_http_client):
    yield gidgethub.aiohttp.GitHubAPI(
        mock_http_client.session,
        requester=GITHUB_USER_ID,
        oauth_token=GITHUB_ACCESS_TOKEN,
    )


@pytest.fixture
async def github_api(mocker, gidgethub_instance):
    mocker.patch("app.github.github_api.settings", Settings.from_yaml("config.sample.yml"))

    return GithubAPI(gidgethub_instance, GITHUB_USER_ID)
