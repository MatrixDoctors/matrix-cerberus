import pickle
from datetime import timedelta
from typing import Any
from uuid import uuid4

from fastapi import Request, Response
from redis import Redis

from app.core.config import get_settings


def generate_id() -> str:
    return uuid4().hex


"""
Redis Session Storage class is used to maintain a connection 
between the redis database and the server.
"""


class RedisSessionStorage:
    def __init__(self):
        self.config = get_settings()
        self.client = Redis.from_url(self.config.redis_dsn)

    def __getitem__(self, key: str):
        raw = self.client.get(key)
        return raw and pickle.loads(raw)

    def __setitem__(self, key: str, value: Any):
        expireTime = timedelta(hours=1)
        self.client.set(
            key,
            pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL),
            ex=self.config.session_expires_in,
        )

    def __delitem__(self, key: str):
        self.client.delete(key)

    def generate_session_id(self) -> str:
        sessionId = generate_id()
        while self.client.exists(sessionId):
            sessionId = generate_id()
        return sessionId


"""
Session Cookie class provides high level methods 
to interact with the redis database
"""


class SessionCookie:
    def __init__(self):
        self.sessions_storage = RedisSessionStorage()
        self.config = get_settings()
        self.session_key = self.config.session_key

    def create_session(self, request: Request, response: Response):
        session_id = self.sessions_storage.generate_session_id()
        data = {"matrix_user": None, "access_token": None}
        self.sessions_storage[session_id] = data

        response.set_cookie(
            key=self.session_key,
            value=session_id,
            httponly=True,
            expires=self.config.session_expires_in,
        )

        return response

    def get_session_id(self, request: Response):
        return request.cookies.get(self.session_key)

    def get_session(self, request: Request):
        session_id = self.get_session_id(request)
        return self.sessions_storage[session_id]

    def set_session(self, request: Request, response: Response, data):
        session_id = self.get_session_id(request)
        self.sessions_storage[session_id] = data
        return response

    def delete_session(self, request: Request, response: Response):
        session_id = self.get_session_id(request)
        if session_id:
            del self.sessions_storage[session_id]
            response.delete_cookie(self.session_key)

        return response
