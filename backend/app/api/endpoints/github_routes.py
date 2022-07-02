from uuid import uuid4

import aiohttp
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import JSONResponse

from app.api.deps import fastapi_sessions, save_user_data
from app.api.models import GithubCode
from app.core.background_runner import matrix_bot_runner
from app.core.config import settings
from app.core.http_client import http_client

router = APIRouter()


@router.get("/login")
async def get_login():

    client_id = settings.github.client_id
    scope = ["read:org", "repo", "read:user"]
    scope = "%20".join(scope)
    redirect_uri = settings.github.redirect_uri
    state = uuid4().hex

    params = {"scope": scope, "client_id": client_id, "redirect_uri": redirect_uri, "state": state}

    url = "https://github.com/login/oauth/authorize?"
    for i in params.keys():
        url = url + f"{i}={params[i]}&"

    # remove trailing '&'
    url = url[:-1]
    print(state)
    return JSONResponse({"url": url, "state": state})


@router.post("/login")
async def authenticate_user(request: Request, body: GithubCode, background_tasks: BackgroundTasks):
    client_id = settings.github.client_id
    client_secret = settings.github.client_secret

    params = {"code": body.code, "client_secret": client_secret, "client_id": client_id}

    url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}

    try:
        async with http_client.session.post(url, params=params, headers=headers) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=422, detail="Invalid code")
            data = await resp.json()

            session_data = fastapi_sessions.get_session(request)
            session_data.github_user_id = "kuries"
            session_data.github_access_token = data["access_token"]
            fastapi_sessions.set_session(request, session_data)

            background_tasks.add_task(save_user_data, session_data)

            return JSONResponse({"message": "success"})
    except aiohttp.ClientConnectionError as err:
        raise HTTPException(status_code=500, detail="Internal server error")
