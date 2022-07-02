from urllib.parse import urljoin

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from app.api.deps import authenticate_user, fastapi_sessions
from app.api.endpoints import external_url, github_routes, users
from app.api.models import OpenIdInfo
from app.core.http_client import http_client
from app.core.models import ServerSessionData
from app.matrix.external_url import ExternalUrlAPI

api_router = APIRouter()

api_router.include_router(
    users.router, prefix="/users", tags=["users"], dependencies=[Depends(authenticate_user)]
)

api_router.include_router(
    external_url.router,
    prefix="/external-url",
    tags=["external url"],
    dependencies=[Depends(authenticate_user), Depends(ExternalUrlAPI)],
)

api_router.include_router(
    github_routes.router,
    prefix="/github",
    tags=["github"],
    dependencies=[Depends(authenticate_user)],
)


@api_router.get("/current-user")
async def current_user(request: Request):
    session_data = fastapi_sessions.get_session(request)
    matrix_user_id, github_user_id = None, None
    if session_data is not None:
        matrix_user_id = session_data.matrix_user
        github_user_id = session_data.github_user_id

    return JSONResponse({"matrix_user_id": matrix_user_id, "github_user_id": github_user_id})


@api_router.post("/verify-openid")
async def verify_openid(open_id_info: OpenIdInfo):
    matrix_homeserver = "https://" + open_id_info.matrix_server_name
    params = {"access_token": open_id_info.access_token}
    url = urljoin(matrix_homeserver, "/_matrix/federation/v1/openid/userinfo")

    try:
        async with http_client.session.get(url, params=params) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=401, detail="Invalid token")
            data = await resp.json()

            server_session_data = ServerSessionData(
                matrix_user=data["sub"], matrix_homeserver=matrix_homeserver
            )

            response = JSONResponse({"message": "success"})

            # Creating a server session with the matrix username.
            session_id, response = fastapi_sessions.create_session(
                response, data=server_session_data
            )

            return response

    except aiohttp.ClientConnectionError as err:
        raise HTTPException(status_code=500, detail="Internal server error")
