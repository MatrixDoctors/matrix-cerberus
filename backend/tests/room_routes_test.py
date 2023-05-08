import json
from unittest import mock

from fastapi.testclient import TestClient
from nio import LoginResponse
from yarl import URL

from app.core.global_app_state import AppState

MATRIX_USER_ID = "@example_user:matrix.org"
GITHUB_USER_ID = "Bob"
ROOM_ID = "@example:matrix.org"


def load_response(filename):
    with open(filename, encoding="utf-8") as f:
        return json.loads(f.read())


async def bot_login(mock_app_state):
    login_response = load_response("tests/data/matrix/login_response.json")
    await mock_app_state.bot_client.receive_response(LoginResponse.from_dict(login_response))
    mock_app_state.bot_client.user_id = MATRIX_USER_ID


async def load_room_to_external_url_object(
    mock_app_state, mock_server, homeserver, event_type, external_url_response
):
    mock_server.get(
        url=f"{homeserver}/_matrix/client/v3/user/{MATRIX_USER_ID}/account_data/{event_type}",
        status=200,
        payload=external_url_response,
    )
    await mock_app_state.bot_client.create_room_to_external_url_mapping()


async def test_get_room_external_urls(
    client_with_no_dependencies, mock_server, mock_app_state: AppState
):
    await bot_login(mock_app_state)

    homeserver = mock_app_state.settings.matrix_bot.homeserver
    app_name = mock_app_state.settings.app_name
    event_type = mock_app_state.bot_client.parse_event_type("external_url", app_name)
    external_url_response = load_response("tests/data/matrix/external_url.json")

    await load_room_to_external_url_object(
        mock_app_state, mock_server, homeserver, event_type, external_url_response
    )

    resp = client_with_no_dependencies.get("/api/rooms/@example:matrix.org/external-url")
    data = resp.json()
    assert data["content"]["permanent"] == "8dfYxp6s"
    assert set(data["content"]["temporary"]) == set(["JzN6dbCm", "iittp1SY"])


async def test_replace_external_url(
    client_with_no_dependencies: TestClient, mock_server, mock_app_state: AppState
):
    await bot_login(mock_app_state)

    homeserver = mock_app_state.settings.matrix_bot.homeserver
    app_name = mock_app_state.settings.app_name
    event_type = mock_app_state.bot_client.parse_event_type("external_url", app_name)
    external_url_response = load_response("tests/data/matrix/external_url.json")

    await load_room_to_external_url_object(
        mock_app_state, mock_server, homeserver, event_type, external_url_response
    )

    url_code = list(mock_app_state.bot_client.room_to_external_url_mapping[ROOM_ID].temporary)[0]

    url_to_set_account_data = (
        f"{homeserver}/_matrix/client/v3/user/{MATRIX_USER_ID}/account_data/{event_type}"
    )
    mock_server.get(
        url=url_to_set_account_data,
        status=200,
        payload=external_url_response,
    )

    mock_server.put(
        url=url_to_set_account_data,
        status=200,
        payload=external_url_response,
    )

    resp = client_with_no_dependencies.post(
        f"/api/rooms/{ROOM_ID}/external-url/replace?url_code={url_code}"
    )
    new_url_code = resp.json()["url_code"]

    assert resp.status_code == 200
    assert new_url_code is not None

    r = mock_server.requests.get(("PUT", URL(url_to_set_account_data)))
    put_request_data = json.loads(r[-1].kwargs["data"])

    # Verify the data being stored in the external url account data event
    assert url_code not in put_request_data["content"]
    assert new_url_code in put_request_data["content"]

    # Verify the data in room_to_external_url_object
    assert url_code not in mock_app_state.bot_client.room_to_external_url_mapping[ROOM_ID].temporary
    assert new_url_code in mock_app_state.bot_client.room_to_external_url_mapping[ROOM_ID].temporary


async def test_delete_external_url(
    client_with_no_dependencies: TestClient, mock_server, mock_app_state: AppState
):
    await bot_login(mock_app_state)

    homeserver = mock_app_state.settings.matrix_bot.homeserver
    app_name = mock_app_state.settings.app_name
    event_type = mock_app_state.bot_client.parse_event_type("external_url", app_name)
    external_url_response = load_response("tests/data/matrix/external_url.json")

    await load_room_to_external_url_object(
        mock_app_state, mock_server, homeserver, event_type, external_url_response
    )

    # Selecting a random url code to delete
    url_code = list(mock_app_state.bot_client.room_to_external_url_mapping[ROOM_ID].temporary)[0]

    url_to_set_account_data = (
        f"{homeserver}/_matrix/client/v3/user/{MATRIX_USER_ID}/account_data/{event_type}"
    )
    mock_server.get(
        url=url_to_set_account_data,
        status=200,
        payload=external_url_response,
    )

    mock_server.put(
        url=url_to_set_account_data,
        status=200,
        payload=external_url_response,
    )

    resp = client_with_no_dependencies.post(
        f"/api/rooms/{ROOM_ID}/external-url/delete?url_code={url_code}"
    )

    assert resp.status_code == 200
    assert resp.json() == {"msg": "success"}

    r = mock_server.requests.get(("PUT", URL(url_to_set_account_data)))
    put_request_data = json.loads(r[-1].kwargs["data"])

    # Verify the data being stored in the external url account data event
    assert url_code not in put_request_data["content"]

    # Verify the data in room_to_external_url_object
    assert url_code not in mock_app_state.bot_client.room_to_external_url_mapping[ROOM_ID].temporary


async def test_create_new_url(
    client_with_no_dependencies: TestClient, mock_server, mock_app_state: AppState
):
    await bot_login(mock_app_state)

    homeserver = mock_app_state.settings.matrix_bot.homeserver
    app_name = mock_app_state.settings.app_name
    event_type = mock_app_state.bot_client.parse_event_type("external_url", app_name)
    external_url_response = load_response("tests/data/matrix/external_url.json")

    await load_room_to_external_url_object(
        mock_app_state, mock_server, homeserver, event_type, external_url_response
    )

    url_to_set_account_data = (
        f"{homeserver}/_matrix/client/v3/user/{MATRIX_USER_ID}/account_data/{event_type}"
    )
    mock_server.get(
        url=url_to_set_account_data,
        status=200,
        payload=external_url_response,
    )

    mock_server.put(
        url=url_to_set_account_data,
        status=200,
        payload=external_url_response,
    )

    use_once_only = True
    resp = client_with_no_dependencies.post(
        f"/api/rooms/{ROOM_ID}/external-url/new?use_once_only={use_once_only}"
    )

    assert resp.status_code == 200
    url_code = resp.json()["urlCode"]

    r = mock_server.requests.get(("PUT", URL(url_to_set_account_data)))
    put_request_data = json.loads(r[-1].kwargs["data"])

    # Verify the data being stored in the external url account data event
    assert url_code in put_request_data["content"]

    # Verify the data in room_to_external_url_object
    assert url_code in mock_app_state.bot_client.room_to_external_url_mapping[ROOM_ID].temporary
