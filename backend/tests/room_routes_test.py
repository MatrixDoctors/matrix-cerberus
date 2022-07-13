import json

import pytest
from nio import LoginResponse

from app.core.global_app_state import AppState
from app.core.models import RoomSpecificExternalUrl

MATRIX_USER_ID = "@example_user:matrix.org"
GITHUB_USER_ID = "Bob"


def load_response(filename):
    with open(filename, encoding="utf-8") as f:
        return json.loads(f.read())


async def test_get_room_external_urls(
    client_with_no_dependencies, mock_server, mock_app_state: AppState
):
    # Login with bot
    login_response = load_response("tests/data/matrix/login_response.json")
    await mock_app_state.bot_client.receive_response(LoginResponse.from_dict(login_response))
    mock_app_state.bot_client.user_id = MATRIX_USER_ID

    # Load external url data from homeserver
    homeserver = mock_app_state.settings.matrix_bot.homeserver
    app_name = mock_app_state.settings.app_name
    event_type = mock_app_state.bot_client.parse_event_type("external_url", app_name)
    external_url_response = load_response("tests/data/matrix/external_url.json")
    mock_server.get(
        url=f"{homeserver}/_matrix/client/v3/user/{MATRIX_USER_ID}/account_data/{event_type}",
        status=200,
        payload=external_url_response,
    )

    await mock_app_state.bot_client.create_room_to_external_url_mapping()

    resp = client_with_no_dependencies.get("/api/rooms/@example:matrix.org/external-url")
    data = resp.json()
    assert data["content"]["permanent"] == "8dfYxp6s"
    assert set(data["content"]["temporary"]) == set(["JzN6dbCm", "iittp1SY"])
