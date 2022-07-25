from fastapi import APIRouter, Request
from starlette.responses import JSONResponse, RedirectResponse

from app.api.deps import fastapi_sessions
from app.core.background_runner import matrix_bot_runner
from app.core.models import ServerSessionData

router = APIRouter()


@router.get("/")
async def message_users():
    return {"message": "Hello User!!!"}


@router.get("/room-list")
async def get_room_list(request: Request):
    session_data = fastapi_sessions.get_session(request)
    resp = await matrix_bot_runner.client.get_rooms_with_mod_permissions(session_data.matrix_user)
    return JSONResponse({"content": resp})


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
    return RedirectResponse("/")
