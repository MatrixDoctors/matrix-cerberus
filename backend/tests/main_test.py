import json

from fastapi.testclient import TestClient

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


def test_user_login():
    response = client.post(
        "api/users/login",
    )
    session_cookie = response.cookies.get_dict()
    assert response.status_code == 200
    assert session_cookie["session"] == "0123456789"
    assert response.json() == {"message": "successfully logged in"}


def test_user_logout():
    response = client.post("api/users/logout", headers={"session": "0123456789"})
    session_cookie = response.cookies.get_dict()
    assert response.status_code == 200
    assert session_cookie == {}
    assert response.json() == {"message": "success"}
