from uuid import uuid4
from datetime import datetime, timedelta

import aiohttp
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import JSONResponse

from app.api.deps import fastapi_sessions, save_user_data
from app.api.models import OAuthCode
from app.core.app_state import app_state

router = APIRouter()


async def get_patreon_user_id(access_token):
    url = "https://www.patreon.com/api/oauth2/api/current_user"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with app_state.http_client.session.get(url, headers=headers) as resp:
        if resp.status != 200:
            raise HTTPException(status_code=422, detail="Error fetching patreon details")
        patreon_details = await resp.json()
        return patreon_details["data"]["attributes"]["email"]


@router.get("/login")
async def get_login():
    client_id = app_state.settings.patreon.client_id
    redirect_uri = app_state.settings.patreon.redirect_uri
    state = uuid4().hex

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state,
    }

    url = f"https://www.patreon.com/oauth2/authorize?"
    for i in params.keys():
        url = url + f"{i}={params[i]}&"

    # remove trailing '&'
    url = url[:-1]
    return JSONResponse({"url": url, "state": state})


@router.post("/login")
async def authenticate_user(request: Request, body: OAuthCode, background_tasks: BackgroundTasks):
    """
    Route for the Patreon Oauth login.

    This method exchanges the secret code with an access token and saves it in the current user's session.
    """
    client_id = app_state.settings.patreon.client_id
    client_secret = app_state.settings.patreon.client_secret

    params = {
        "code": body.code,
        "grant_type": "authorization_code",
        "client_secret": client_secret,
        "client_id": client_id,
        "redirect_uri": app_state.settings.patreon.redirect_uri,
    }

    url = "https://www.patreon.com/api/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        async with app_state.http_client.session.post(url, params=params, headers=headers) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=422, detail="Invalid code")
            data = await resp.json()
            print(data)

            session_data = fastapi_sessions.get_session(request)

            session_data.patreon_user_id = await get_patreon_user_id(data["access_token"])
            session_data.patreon_access_token = data["access_token"]
            session_data.patreon_refresh_token = data["refresh_token"]

            # Calculate expire date and store it in iso format.
            expire_date = datetime.now() + timedelta(seconds=data["expires_in"])
            session_data.patreon_expire_date = expire_date.isoformat()

            fastapi_sessions.set_session(request, session_data)

            background_tasks.add_task(save_user_data, session_data)

            return JSONResponse({"message": "success"})
    except aiohttp.ClientConnectionError as err:
        raise HTTPException(status_code=500, detail="Internal server error")
