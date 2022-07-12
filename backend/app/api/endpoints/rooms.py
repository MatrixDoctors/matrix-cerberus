from fastapi import APIRouter, Depends
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
async def delete_external_url(
    room_id: str, url_code: str, external_url: ExternalUrlAPI = Depends(external_url_api_instance)
):
    new_url_code = await external_url.replace_existing_url(url_code)
    return JSONResponse({"url_code": new_url_code})
