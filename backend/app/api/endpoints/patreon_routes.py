import urllib
from uuid import uuid4
from datetime import datetime, timedelta

import aiohttp
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from app.api.deps import (
    fastapi_sessions,
    patreon_api_instance,
    save_user_data,
    verify_room_permissions,
)
from app.api.models import OAuthCode
from app.core.app_state import app_state
from app.core.models import PatreonCampaignConditions, PatreonCampaignTier
from app.patreon.patreon_api import PatreonAPI

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

    scope = ["identity", "identity[email]", "identity.memberships", "campaigns"]
    scope = " ".join(scope)
    scope = urllib.parse.quote(scope)

    state = uuid4().hex

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": scope,
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


@router.get("/{room_id}/patreon/campaign", dependencies=[Depends(verify_room_permissions)])
async def get_patreon_campaign_conditions(
    room_id: str, patreon_api: PatreonAPI = Depends(patreon_api_instance)
):
    """
    API Route to fetch patreon conditions of a campaign owned by the authorized user.
    """
    resp = await app_state.bot_client.get_account_data(type="rooms", room_id=room_id)

    data_to_be_sent = None

    for campaign_id, campaign_data in resp.content.patreon.campaigns.items():
        if patreon_api.email == campaign_data.belongs_to:
            data_to_be_sent = {"id": campaign_id, "attributes": campaign_data.dict()}
            break

    if data_to_be_sent is None:
        data_to_be_sent = await patreon_api.campaign_information()

    return JSONResponse({"content": data_to_be_sent})


@router.put("/{room_id}/patreon/campaign", dependencies=[Depends(verify_room_permissions)])
async def get_patreon_campaign_conditions(
    room_id: str, patreon_api: PatreonAPI = Depends(patreon_api_instance)
):
    pass


@router.get("/tiers", dependencies=[Depends(verify_room_permissions)])
async def get_tiers(request: Request, patreon_api: PatreonAPI = Depends(patreon_api_instance)):
    resp = await patreon_api.tiers_of_all_campaigns()
    return JSONResponse({"content": resp})
