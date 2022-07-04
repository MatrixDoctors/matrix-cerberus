import json

import pytest
from aioresponses import aioresponses
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.http_client import http_client
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_server():
    with aioresponses() as m:
        yield m


def test_main():
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_message_users():
    response = client.get("api/users")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello User!!!"}


@pytest.mark.asyncio
async def test_user_session_flow(mock_server):
    matrix_user = "@example_user:matrix.org"
    http_client.start_session()

    mock_server.get(
        url="https://matrix.org/_matrix/federation/v1/openid/userinfo?access_token=some_access_token",
        status=200,
        payload={"sub": matrix_user},
    )

    open_id_data = {
        "access_token": "some_access_token",
        "expires_in": 3600,
        "matrix_server_name": "matrix.org",
        "token_type": "Bearer",
    }
    response = client.post("api/users/verify-openid", data=json.dumps(open_id_data))
    session_cookie = response.cookies.get_dict()
    assert response.status_code == 200
    assert session_cookie[settings.server_sessions.session_key] is not None
    assert response.json() == {"message": "success"}

    # Check the saved details of the user
    response = client.post("api/users/printToken")
    assert response.status_code == 200
    assert response.json() == {"matrix_user": matrix_user}

    # Client logs out
    response = client.post(
        "api/users/logout",
    )

    assert response.status_code == 200
    session_cookie = response.cookies.get_dict()
    assert settings.server_sessions.session_key not in session_cookie
    assert response.json() == {"message": "success"}
