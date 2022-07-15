from urllib.parse import urljoin

import aiohttp
from fastapi import APIRouter, HTTPException, Request
from starlette.responses import JSONResponse, RedirectResponse

from app.api.deps import fastapi_sessions
from app.api.models import OpenIdInfo
from app.core.http_client import http_client
from app.core.models import ServerSessionData

router = APIRouter()


@router.get("/")
async def message_users():
    return {"message": "Hello User!!!"}


@router.post("/verify-openid")
async def verify_openid(request: Request, open_id_info: OpenIdInfo):
    matrix_homeserver = "https://" + open_id_info.matrix_server_name
    params = {"access_token": open_id_info.access_token}
    url = urljoin(matrix_homeserver, "/_matrix/federation/v1/openid/userinfo")

    try:
        async with http_client.session.get(url, params=params) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=404, detail="Invalid token")
            data = await resp.json()

            server_session_data = ServerSessionData(
                matrix_user=data["sub"], matrix_homeserver=matrix_homeserver
            )

            response = JSONResponse({"message": "success"})
            # Creating a server session with the matrix username.
            response = fastapi_sessions.create_session(response, data=server_session_data)
            return response

    except aiohttp.ClientConnectionError as err:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/logout")
async def logout(request: Request):
    response = JSONResponse({"message": "success"})
    response = fastapi_sessions.delete_session(request, response)
    return response


@router.post("/changeTokens")
async def change_tokens(request: Request, name: str):
    data = ServerSessionData(matrix_user=name)
    fastapi_sessions.set_session(request, data)
    response = JSONResponse({"message": "success"})
    return response


@router.post("/printToken")
async def change_tokens(request: Request):
    data = fastapi_sessions.get_session(request)
    response = JSONResponse({"matrix_user": f"{data.matrix_user}"})
    return response


# Redirects to the React Home page
@router.get("/redirect")
async def redirect():
    response = RedirectResponse(url="/")
    return response
