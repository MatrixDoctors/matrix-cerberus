import pickle
from uuid import uuid4
from typing import Any

from fastapi import Request, Response
from redis import Redis

from app.core.config import settings


def generate_id() -> str:
    return uuid4().hex


class RedisSessionStorage:
    """
    Redis Session Storage class is used to maintain a connection
    between the redis database and the server.
    """

    def __init__(self):
        self.client = Redis.from_url(settings.redis.uri)

    def __getitem__(self, key: str):
        raw = self.client.get(key)
        return raw and pickle.loads(raw)

    def __setitem__(self, key: str, value: Any):
        self.client.set(
            key,
            pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL),
        )

    def __delitem__(self, key: str):
        self.client.delete(key)

    def set_item_with_expiry_time(self, key: str, value: Any, expires_in: int = None):
        self.client.set(
            key,
            pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL),
            ex=expires_in,
        )

    def generate_session_id(self) -> str:
        sessionId = generate_id()
        while self.client.exists(sessionId):
            sessionId = generate_id()
        return sessionId


session_storage = RedisSessionStorage()


class SessionCookie:
    """
    Session Cookie class provides high level methods
    to interact with the redis database
    """

    def __init__(self):
        self.session_storage = session_storage
        self.session_key = settings.server_sessions.session_key
        self.expires_in = settings.server_sessions.expires_in

    def create_session(self, response: Response):
        session_id = self.session_storage.generate_session_id()
        data = {"matrix_user": None, "access_token": None}
        self.session_storage.set_item_with_expiry_time(
            key=session_id, value=data, expires_in=self.expires_in
        )

        response.set_cookie(
            key=self.session_key,
            value=session_id,
            httponly=True,
            expires=settings.server_sessions.expires_in,
        )

        return response

    def get_session_id(self, request: Response):
        return request.cookies.get(self.session_key)

    def get_session(self, request: Request):
        session_id = self.get_session_id(request)
        return self.session_storage[session_id]

    def set_session(self, request: Request, data):
        session_id = self.get_session_id(request)
        self.session_storage.set_item_with_expiry_time(
            key=session_id, value=data, expires_in=self.expires_in
        )

    def delete_session(self, request: Request, response: Response):
        session_id = self.get_session_id(request)
        if session_id:
            del self.session_storage[session_id]
            response.delete_cookie(self.session_key)

        return response
