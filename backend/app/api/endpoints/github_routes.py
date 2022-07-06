from uuid import uuid4

import aiohttp
import gidgethub.aiohttp
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from app.api.deps import fastapi_sessions, github_api_instance, save_user_data
from app.api.models import GithubCode
from app.core.config import settings
from app.core.http_client import http_client
from app.github.github_api import GithubAPI

router = APIRouter()


async def get_github_user_id(access_token):
    gh = gidgethub.aiohttp.GitHubAPI(
        http_client.session, requester="matrix-cerberus", oauth_token=access_token
    )
    user_object = await gh.getitem("/user")
    return user_object["login"]


@router.get("/login")
async def get_login():

    client_id = settings.github.client_id
    scope = ["read:org", "repo", "user"]
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

            session_data.github_user_id = await get_github_user_id(data["access_token"])
            session_data.github_access_token = data["access_token"]
            print(data["access_token"])
            fastapi_sessions.set_session(request, session_data)

            background_tasks.add_task(save_user_data, session_data)

            return JSONResponse({"message": "success"})
    except aiohttp.ClientConnectionError as err:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/user")
async def get_user(github_api: GithubAPI = Depends(github_api_instance)):
    resp = await github_api.display_user()
    return JSONResponse({"user": resp})


@router.get("/orgs")
async def get_orgs(github_api: GithubAPI = Depends(github_api_instance)):
    resp = await github_api.get_orgs_with_membership()
    return JSONResponse({"orgs": resp})


@router.get("/individual-repos")
async def get_individual_repos(github_api: GithubAPI = Depends(github_api_instance)):
    resp = await github_api.get_individual_repos()
    return JSONResponse({"repos": resp})


@router.get("/org-repos")
async def get_org_repos(org: str, github_api: GithubAPI = Depends(github_api_instance)):
    resp = await github_api.get_repos_in_an_org(org)
    return JSONResponse({"repos": resp})


@router.get("/org-teams")
async def get_org_teams(org: str, github_api: GithubAPI = Depends(github_api_instance)):
    resp = await github_api.get_teams_in_an_org(org)
    return JSONResponse({"teams": resp})
