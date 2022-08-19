from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.responses import JSONResponse

from app.api.deps import (
    external_url_api_instance,
    fastapi_sessions,
    github_api_instance,
    verify_room_permissions,
)
from app.api.models import OwnerField, RoomConditions
from app.core.app_state import app_state
from app.core.models import (
    GithubConditions,
    GithubOrganisationConditions,
    GithubRepositoryConditions,
    GithubUserConditions,
)
from app.github.github_api import GithubAPI
from app.matrix.external_url import ExternalUrlAPI

router = APIRouter()


async def parse_github_org_data(github_conditions: GithubConditions):
    orgs = github_conditions.orgs
    owner_type = "org"
    list_of_conditions = []
    for org_name, org_data in orgs.items():
        for repo_name, repo_data in org_data.repos.items():
            repo_condition = RoomConditions(
                type=owner_type,
                third_party_account="Github",
                owner={"parent": org_name, "child": repo_name},
                condition_type="Repository",
                data=repo_data,
            )
            list_of_conditions.append(repo_condition.dict())

        if org_data.teams:
            list_of_conditions.append(
                RoomConditions(
                    type=owner_type,
                    third_party_account="Github",
                    owner={
                        "parent": org_name,
                    },
                    condition_type="Teams",
                    data=org_data.teams,
                ).dict()
            )

        if org_data.sponsorship_tiers:
            list_of_conditions.append(
                RoomConditions(
                    type=owner_type,
                    third_party_account="Github",
                    owner={
                        "parent": org_name,
                    },
                    condition_type="Sponsorship Tiers",
                    data=org_data.sponsorship_tiers,
                ).dict()
            )

    return list_of_conditions


async def parse_github_user_data(user_name: str, github_conditions: GithubConditions):
    owner_type = "user"
    list_of_conditions = []

    if user_name in github_conditions.users:
        user_data = github_conditions.users[user_name]

        for repo_name, repo_data in user_data.repos.items():
            repo_condition = RoomConditions(
                type=owner_type,
                third_party_account="Github",
                owner={"parent": user_name, "child": repo_name},
                condition_type="Repository",
                data=repo_data,
            )
            list_of_conditions.append(repo_condition.dict())

        if user_data.sponsorship_tiers:
            list_of_conditions.append(
                RoomConditions(
                    type=owner_type,
                    third_party_account="Github",
                    owner={
                        "parent": user_name,
                    },
                    condition_type="Sponsorship Tiers",
                    data=user_data.sponsorship_tiers,
                ).dict()
            )

    return list_of_conditions


@router.get("/{room_id}", dependencies=[Depends(verify_room_permissions)])
async def get_room_conditions(request: Request, room_id: str):
    resp = await app_state.bot_client.get_account_data(type="rooms", room_id=room_id)

    session_data = fastapi_sessions.get_session(request)
    github_username = session_data.github_user_id

    list_of_conditions = []
    list_of_conditions.extend(await parse_github_org_data(resp.content.github))
    list_of_conditions.extend(
        await parse_github_user_data(
            user_name=github_username, github_conditions=resp.content.github
        )
    )
    return JSONResponse(list_of_conditions)


@router.post(
    "/{room_id}/github/{owner_type}/{condition_type}",
    dependencies=[Depends(verify_room_permissions)],
)
async def get_github_room_condition(
    room_id: str,
    owner_type: str,
    condition_type: str,
    owner: OwnerField,
    github_api: GithubAPI = Depends(github_api_instance),
):
    """
    API Route to fetch github conditions of a specific type under a particular owner (user/org).
    """
    resp = await app_state.bot_client.get_account_data(type="rooms", room_id=room_id)

    if owner_type == "org":
        github_data = resp.content.github.orgs
    elif owner_type == "user":
        github_data = resp.content.github.users
    else:
        raise HTTPException(status_code=400, detail="Invalid owner type")

    data_to_be_sent = None

    if condition_type == "repository":
        if owner.parent in github_data and owner.child in github_data[owner.parent].repos:
            data_to_be_sent = github_data[owner.parent].repos[owner.child]
        else:
            data_to_be_sent = GithubRepositoryConditions()
        data_to_be_sent = data_to_be_sent.dict()
    elif condition_type == "teams" and owner_type == "org":
        if owner.parent in github_data and github_data[owner.parent].teams:
            data_to_be_sent = github_data[owner.parent].teams
        else:
            teams = await github_api.get_teams_in_an_org(owner.parent)
            data_to_be_sent = {team_slug: False for team_slug in teams.keys()}
    elif condition_type == "sponsorship tiers":
        if owner.parent in github_data and github_data[owner.parent].sponsorship_tiers:
            data_to_be_sent = github_data[owner.parent].sponsorship_tiers
        else:
            if owner_type == "org":
                tiers = await github_api.get_sponsorship_tiers_for_org(owner.parent)
            else:
                tiers = await github_api.get_sponsorship_tiers_for_user(owner.parent)
            data_to_be_sent = {tier_name: False for tier_name in tiers}
    else:
        raise HTTPException(status_code=400, detail="Invalid condition type sent.")

    return JSONResponse({"content": data_to_be_sent})


@router.put(
    "/{room_id}/github/{owner_type}/{condition_type}",
    dependencies=[Depends(verify_room_permissions)],
)
async def put_github_room_condition(
    request: Request,
    room_id: str,
    owner_type: str,
    condition_type: str,
    room_conditions: RoomConditions,
):
    """
    API Route to save github conditions of a specific type under a particular owner (user/org).

    It stores the updated data in the 'rooms' bot account data event.
    """
    resp = await app_state.bot_client.get_account_data(type="rooms", room_id=room_id)

    owner_name = room_conditions.owner.parent
    user_session = fastapi_sessions.get_session(request)
    logged_in_user = user_session.matrix_user

    if owner_type == "org":
        github_data = resp.content.github.orgs
        if owner_name not in github_data:
            github_data[owner_name] = GithubOrganisationConditions()

        github_data[owner_name].last_edited_by = logged_in_user
    else:
        github_data = resp.content.github.users
        if owner_name not in github_data:
            github_data[owner_name] = GithubUserConditions()

    if condition_type == "repository":
        repo_name = room_conditions.owner.child
        github_data[owner_name].repos[repo_name] = room_conditions.data
    elif condition_type == "teams":
        github_data[owner_name].teams = room_conditions.data
    elif condition_type == "sponsorship tiers":
        github_data[owner_name].sponsorship_tiers = room_conditions.data
    else:
        raise HTTPException(status_code=400, detail="Invalid condition type sent.")

    resp = await app_state.bot_client.put_account_data(type="rooms", data=resp, room_id=room_id)
    return JSONResponse({"msg": "success"})


@router.post(
    "/{room_id}/github/{owner_type}/{condition_type}/delete",
    dependencies=[Depends(verify_room_permissions)],
)
async def delete_github_room_condition(
    room_id: str, owner_type: str, condition_type: str, room_conditions: RoomConditions
):
    """
    API Route to delete a github condition in the 'rooms' bot account data event.
    """
    resp = await app_state.bot_client.get_account_data(type="rooms", room_id=room_id)

    if owner_type == "org":
        github_data = resp.content.github.orgs
    else:
        github_data = resp.content.github.users

    owner_name = room_conditions.owner.parent

    if condition_type == "repository":
        repo_name = room_conditions.owner.child
        del github_data[owner_name].repos[repo_name]
    elif condition_type == "teams":
        github_data[owner_name].teams = dict()
    elif condition_type == "sponsorship tiers":
        github_data[owner_name].sponsorship_tiers = dict()
    else:
        raise HTTPException(status_code=400, detail="Invalid condition type sent.")

    resp = await app_state.bot_client.put_account_data(type="rooms", data=resp, room_id=room_id)
    return JSONResponse({"msg": "success"})


@router.post("/{room_id}/patreon/campaign", dependencies=[Depends(verify_room_permissions)])
async def get_patreon_campaign_conditions(room_id: str):
    pass


@router.put("/{room_id}/disable-room-kick/edit", dependencies=[Depends(verify_room_permissions)])
async def edit_room_disable_kick_option(room_id: str, disable_room_kick: bool):

    resp = await app_state.bot_client.get_account_data(type="rooms", room_id=room_id)
    resp.content.disable_room_kick = disable_room_kick
    del resp.content.github.orgs["kuries"]
    resp = await app_state.bot_client.put_account_data(type="rooms", data=resp, room_id=room_id)
    return JSONResponse({"msg": "success"})


@router.get("/{room_id}/external-url", dependencies=[Depends(verify_room_permissions)])
async def get_room_external_urls(
    room_id: str, external_url: ExternalUrlAPI = Depends(external_url_api_instance)
):
    """
    Method to edit the room kick option for a room.
    """
    resp = await external_url.get_room_external_url(room_id)
    return JSONResponse(
        {"content": {"permanent": resp.permanent, "temporary": list(resp.temporary)}}
    )


@router.post("/{room_id}/external-url/replace", dependencies=[Depends(verify_room_permissions)])
async def replace_external_url(
    room_id: str, url_code: str, external_url: ExternalUrlAPI = Depends(external_url_api_instance)
):
    new_url_code = await external_url.replace_existing_url(url_code)
    return JSONResponse({"url_code": new_url_code})


@router.post("/{room_id}/external-url/delete", dependencies=[Depends(verify_room_permissions)])
async def delete_external_url(
    room_id: str, url_code: str, external_url: ExternalUrlAPI = Depends(external_url_api_instance)
):
    try:
        await external_url.delete_url(url_code)
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid URL Code")

    return JSONResponse({"msg": "success"})


@router.post("/{room_id}/external-url/new", dependencies=[Depends(verify_room_permissions)])
async def create_new_url(
    room_id: str,
    use_once_only: bool,
    external_url: ExternalUrlAPI = Depends(external_url_api_instance),
):
    url_code = await external_url.generate_url(
        room_id=room_id,
        use_once_only=use_once_only,
    )
    return JSONResponse({"urlCode": url_code})
