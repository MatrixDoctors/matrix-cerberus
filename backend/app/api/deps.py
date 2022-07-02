from fastapi import HTTPException, Request

from app.core.background_runner import matrix_bot_runner
from app.core.http_client import http_client
from app.core.models import ServerSessionData
from app.core.sessions import SessionCookie, session_storage

fastapi_sessions = SessionCookie()


async def authenticate_user(request: Request):
    if fastapi_sessions.get_session(request) is None:
        raise HTTPException(status_code=401, detail="Not authorized")


async def fetch_user_data(session_id):
    session_data: ServerSessionData = session_storage[session_id]
    resp = await matrix_bot_runner.client.get_account_data("user", user_id=session_data.matrix_user)

    session_data.github_user_id = resp.content.github.username
    session_data.github_access_token = resp.content.github.access_token

    session_data.patreon_user_id = resp.content.patreon.email
    session_data.patreon_access_token = resp.content.patreon.access_token

    session_storage[session_id] = session_data
    pass
