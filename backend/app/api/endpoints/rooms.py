from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from app.api.deps import (
    external_url_api_instance,
    fastapi_sessions,
    verify_room_permissions,
)
from app.matrix.external_url import ExternalUrlAPI

router = APIRouter()


@router.get("/{room_id}/external-url", dependencies=[Depends(verify_room_permissions)])
async def get_room_external_urls(
    room_id: str, external_url: ExternalUrlAPI = Depends(external_url_api_instance)
):
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
