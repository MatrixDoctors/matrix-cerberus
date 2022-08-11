"""
This module consists of all the dependencies, background tasks and instances of classes that will be required by the path functions.
"""

import gidgethub.aiohttp
from fastapi import Depends, HTTPException, Request

from app.core.background_runner import matrix_bot_runner
from app.core.http_client import http_client
from app.core.models import ServerSessionData, UserData
from app.core.sessions import SessionCookie, session_storage
from app.github.github_api import GithubAPI

fastapi_sessions = SessionCookie()


async def authenticate_user(request: Request):
    if fastapi_sessions.get_session(request) is None:
        raise HTTPException(status_code=401, detail="Not authorized")


async def fetch_user_data(session_id, session_data: ServerSessionData):
    resp = await matrix_bot_runner.client.get_account_data("user", user_id=session_data.matrix_user)

    session_data.github_user_id = resp.content.github.username
    session_data.github_access_token = resp.content.github.access_token

    session_data.patreon_user_id = resp.content.patreon.email
    session_data.patreon_access_token = resp.content.patreon.access_token

    session_storage[session_id] = session_data


async def save_user_data(session_data: ServerSessionData):
    data = UserData()
    data.content.github.username = session_data.github_user_id
    data.content.github.access_token = session_data.github_access_token

    data.content.patreon.email = session_data.patreon_access_token
    data.content.patreon.access_token = session_data.patreon_access_token

    await matrix_bot_runner.client.put_account_data(
        type="user", data=data, user_id=session_data.matrix_user
    )


async def gidgethub_instance(request: Request):
    session_data = fastapi_sessions.get_session(request)
    return gidgethub.aiohttp.GitHubAPI(
        http_client.session,
        requester=session_data.github_user_id,
        oauth_token=session_data.github_access_token,
    )


async def github_api_instance(
    request: Request, gh: gidgethub.aiohttp.GitHubAPI = Depends(gidgethub_instance)
):
    session_data = fastapi_sessions.get_session(request)
    github_api = GithubAPI(gh, session_data.github_user_id)
    return github_api
