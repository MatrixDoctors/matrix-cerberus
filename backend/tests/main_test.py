from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)


def test_main():
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_message_users():
    response = client.get("api/users")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello User!!!"}


def test_user_session_flow():
    # Client logs in.
    response = client.post(
        "api/users/login",
    )
    session_cookie = response.cookies.get_dict()
    assert response.status_code == 200
    assert session_cookie[settings.server_sessions.session_key] is not None
    assert response.json() == {"message": "successfully logged in"}

    # Set the 'matrix_user' field in session database
    name = "John Paul"
    params = {"name": name}
    response = client.post("api/users/changeTokens", params=params)

    assert response.status_code == 200
    assert response.json() == {"message": "success"}

    # fetch the 'matrix_user' field in session database
    response = client.post("api/users/printToken")
    assert response.status_code == 200
    assert response.json() == {"matrix_user": name}

    # Client logs out
    response = client.post(
        "api/users/logout",
    )

    assert response.status_code == 200
    session_cookie = response.cookies.get_dict()
    assert settings.server_sessions.session_key not in session_cookie
    assert response.json() == {"message": "success"}
