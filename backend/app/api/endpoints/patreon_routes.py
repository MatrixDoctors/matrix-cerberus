from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import JSONResponse

from app.api.models import OAuthCode
from app.core.app_state import app_state

router = APIRouter()


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
    print(body)
    return JSONResponse({"message": "success"})
