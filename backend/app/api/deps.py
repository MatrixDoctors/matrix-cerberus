from fastapi import HTTPException, Request

from app.core.background_runner import matrix_bot_runner
from app.core.http_client import http_client
from app.core.sessions import SessionCookie

fastapi_sessions = SessionCookie()


async def authenticate_user(request: Request):
    if fastapi_sessions.get_session(request) is None:
        raise HTTPException(status_code=401, detail="Not authorized")
