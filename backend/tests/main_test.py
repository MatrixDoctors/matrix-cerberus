import json

import pytest


def test_main(client):
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_message_users(client):
    # Verify authentication checks
    response = client.get("api/users")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authorized"}


@pytest.mark.asyncio
async def test_user_session_flow(mocker, client, mock_server, mock_http_client, settings):
    # mock_http_client is imported to start the aiohttp session.

    mock_fetch_user_data = mocker.patch('app.api.api.fetch_user_data')

    matrix_user = "@example_user:matrix.org"

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
    response = client.post("api/verify-openid", data=json.dumps(open_id_data))
    session_cookie = response.cookies.get_dict()

    assert response.status_code == 200
    assert session_cookie[settings.server_sessions.session_key] is not None
    assert response.json() == {"message": "success"}
    assert mock_fetch_user_data.call_count == 1

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
