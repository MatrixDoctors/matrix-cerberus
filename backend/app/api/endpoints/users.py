import typing as t
from urllib import response
from urllib.parse import urljoin

import aiohttp
from fastapi import APIRouter, Depends, Form, HTTPException, Request, encoders
from starlette.responses import JSONResponse, RedirectResponse, Response

from app.api.deps import fastapi_sessions
from app.api.models import OpenIdInfo
from app.core.aiohttp_session import AioHttpSession

router = APIRouter()


@router.get("/")
async def message_users():
    return {"message": "Hello User!!!"}


@router.post("/verify-openid")
async def verify_openid(request: Request, open_id_info: OpenIdInfo):
    session = AioHttpSession().session

    matrix_homeserver = "https://" + open_id_info.matrix_server_name
    params = {"access_token": open_id_info.access_token}
    url = urljoin(matrix_homeserver, "/_matrix/federation/v1/openid/userinfo")

    try:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=404, detail="Invalid token")
            data = await resp.json()
            response = JSONResponse({"message": "success"})
            response = fastapi_sessions.create_session(request, response)
            return response
    except aiohttp.ClientConnectionError as err:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/login")
async def login(request: Request):
    response = JSONResponse({"message": "successfully logged in"})
    response = fastapi_sessions.create_session(request, response)
    return response


@router.post("/logout")
async def logout(request: Request):
    response = JSONResponse({"message": "success"})
    response = fastapi_sessions.delete_session(request, response)
    return response


@router.post("/changeTokens")
async def change_tokens(request: Request, name: str):
    data = fastapi_sessions.get_session(request)
    data["matrix_user"] = f"{name}"
    response = JSONResponse({"message": "success"})
    response = fastapi_sessions.set_session(request, response, data)
    return response


@router.post("/printToken")
async def change_tokens(request: Request):
    data = fastapi_sessions.get_session(request)
    response = JSONResponse({"matrix_user": f"{data['matrix_user']}"})
    response = fastapi_sessions.set_session(request, response, data)
    return response


# Redirects to the React Home page
@router.get("/redirect")
async def redirect():
    response = RedirectResponse(url="/")
    return response
