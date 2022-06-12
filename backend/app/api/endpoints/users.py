import typing as t
from urllib import response

from fastapi import APIRouter, Depends, Form, Request, encoders
from starlette.responses import JSONResponse, RedirectResponse, Response

from app.core.sessions import SessionCookie

fastapi_sessions = SessionCookie()
router = APIRouter()


@router.get("/")
async def message_users():
    return {"message": "Hello User!!!"}


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
