"""
This module consists of all the dependencies, background tasks and instances of classes that will be required by the path functions.

Any authentication and permission checks to be made before accessing an endpoint go here.
"""

import gidgethub.aiohttp
from fastapi import Depends, HTTPException, Request

from app.core.app_state import app_state
from app.core.models import ServerSessionData, UserData
from app.github.github_api import GithubAPI
from app.matrix.external_url import ExternalUrlAPI

fastapi_sessions = app_state.server_session


async def authenticate_user(request: Request):
    if fastapi_sessions.get_session(request) is None:
        raise HTTPException(status_code=401, detail="Not authorized")


async def verify_room_permissions(request: Request, room_id: str):
    session_data: ServerSessionData = fastapi_sessions.get_session(request)

    if room_id in app_state.bot_client.rooms:
        room_object = app_state.bot_client.rooms[room_id]
        if room_object.power_levels.get_user_level(session_data.matrix_user) < 50:
            raise HTTPException(status_code=400, detail="User dosen't satisfy room permissions")
    else:
        raise HTTPException(status_code=400, detail="Bot is not part of the room")


async def fetch_user_data(session_id, session_data: ServerSessionData):
    resp = await app_state.bot_client.get_account_data("user", user_id=session_data.matrix_user)

    session_data.github_user_id = resp.content.github.username
    session_data.github_access_token = resp.content.github.access_token

    session_data.patreon_user_id = resp.content.patreon.email
    session_data.patreon_access_token = resp.content.patreon.access_token

    app_state.session_storage[session_id] = session_data


async def save_user_data(session_data: ServerSessionData):
    data = UserData()
    data.content.github.username = session_data.github_user_id
    data.content.github.access_token = session_data.github_access_token

    data.content.patreon.email = session_data.patreon_access_token
    data.content.patreon.access_token = session_data.patreon_access_token

    await app_state.bot_client.put_account_data(
        type="user", data=data, user_id=session_data.matrix_user
    )


async def gidgethub_instance(request: Request) -> gidgethub.aiohttp.GitHubAPI:
    session_data = fastapi_sessions.get_session(request)
    return gidgethub.aiohttp.GitHubAPI(
        app_state.http_client.session,
        requester=session_data.github_user_id,
        oauth_token=session_data.github_access_token,
    )


async def github_api_instance(
    request: Request, gh: gidgethub.aiohttp.GitHubAPI = Depends(gidgethub_instance)
) -> GithubAPI:
    session_data = fastapi_sessions.get_session(request)
    github_api = GithubAPI(
        gh=gh,
        username=session_data.github_user_id,
        default_role=app_state.settings.github.organisation_membership,
    )
    return github_api


async def external_url_api_instance() -> ExternalUrlAPI:
    return ExternalUrlAPI(app_state.bot_client)
