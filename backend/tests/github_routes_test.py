import json
from unittest import mock

import pytest

MATRIX_USER_ID = "@example_user:matrix.org"
GITHUB_USER_ID = "Bob"


@pytest.fixture
async def logged_in_client(mocker, client, mock_server, mock_app_state):
    # mock_app_state is imported to start the http_client session
    mocker.patch("app.api.api.fetch_user_data")

    mock_server.get(
        url="https://matrix.org/_matrix/federation/v1/openid/userinfo?access_token=some_access_token",
        status=200,
        payload={"sub": MATRIX_USER_ID},
    )

    open_id_data = {
        "access_token": "some_access_token",
        "expires_in": 3600,
        "matrix_server_name": "matrix.org",
        "token_type": "Bearer",
    }

    response = client.post("api/verify-openid", data=json.dumps(open_id_data))
    assert response.status_code == 200

    yield client

    response = client.post("api/users/logout")
    assert response.status_code == 200


async def test_get_login(mocker, logged_in_client, mock_app_state):
    uuid = mock.Mock()
    uuid.hex = "abc123"
    mocker.patch("app.api.endpoints.github_routes.uuid4", return_value=uuid)

    settings = mock_app_state.settings

    scope = ["read:org", "repo", "user"]
    scope = "%20".join(scope)

    url = f"https://github.com/login/oauth/authorize?scope={scope}&client_id={settings.github.client_id}&redirect_uri={settings.github.redirect_uri}&state={uuid.hex}"

    response = logged_in_client.get("api/github/login")
    data = response.json()
    assert data["url"] == url
    assert data["state"] == uuid.hex


async def test_post_login(mocker, logged_in_client, mock_server, mock_app_state):
    mocker.patch("app.api.endpoints.github_routes.get_github_user_id", return_value=GITHUB_USER_ID)
    m_save_user_data = mocker.patch("app.api.endpoints.github_routes.save_user_data")

    settings = mock_app_state.settings

    client_id = settings.github.client_id
    client_secret = settings.github.client_secret
    body = {"code": "abc123"}

    url = f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={body['code']}"
    payload_data = {
        "access_token": "some_access_token",
        "scope": "some_scopes",
        "token_type": "bearer",
    }

    mock_server.post(url, status=200, payload=payload_data)

    response = logged_in_client.post("api/github/login", data=json.dumps(body))
    assert response.status_code == 200

    response = logged_in_client.get("api/current-user")
    assert response.status_code == 200
    assert response.json() == {"matrix_user_id": MATRIX_USER_ID, "github_user_id": GITHUB_USER_ID}
    assert m_save_user_data.call_count == 1


async def test_failed_post_login(mocker, logged_in_client, mock_server, mock_app_state):
    mocker.patch("app.api.endpoints.github_routes.get_github_user_id", return_value=GITHUB_USER_ID)

    settings = mock_app_state.settings

    client_id = settings.github.client_id
    client_secret = settings.github.client_secret
    body = {"code": "abc123"}

    url = f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={body['code']}"

    mock_server.post(url, status=422, payload={"detail": "Invalid credentials"})

    response = logged_in_client.post("api/github/login", data=json.dumps(body))
    assert response.status_code == 422
