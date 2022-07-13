import gidgethub.aiohttp
import pytest
from aioresponses import aioresponses
from fastapi.testclient import TestClient

from app.api.deps import authenticate_user, verify_room_permissions
from app.core.global_app_state import AppState
from app.github.github_api import GithubAPI
from app.main import app

from .override_dependency import DependencyOverrider

GITHUB_USER_ID = "p0tato"
GITHUB_ACCESS_TOKEN = "some_access_token"


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def client_with_no_dependencies():
    async def dummy_func():
        pass

    with DependencyOverrider(
        app, overrides={verify_room_permissions: dummy_func, authenticate_user: dummy_func}
    ) as overrider:
        yield TestClient(app)


@pytest.fixture
async def mock_app_state():
    from app.core.app_state import app_state

    await app_state.http_client.start_session()
    yield app_state
    await app_state.http_client.stop_session()


@pytest.fixture
def mock_server():
    with aioresponses() as m:
        yield m


@pytest.fixture
async def gidgethub_instance(mock_app_state):
    yield gidgethub.aiohttp.GitHubAPI(
        mock_app_state.http_client.session,
        requester=GITHUB_USER_ID,
        oauth_token=GITHUB_ACCESS_TOKEN,
    )


@pytest.fixture
async def github_api(mock_app_state: AppState, gidgethub_instance):
    return GithubAPI(
        gh=gidgethub_instance,
        username=GITHUB_USER_ID,
        default_role=mock_app_state.settings.github.organisation_membership,
    )
