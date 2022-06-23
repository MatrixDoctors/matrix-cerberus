from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse

from app.api.deps import fastapi_sessions
from app.api.models import ExternalUrlInfo
from app.matrix.external_url import ExternalUrl

router = APIRouter()


@router.post("/generate-url")
async def generate_url(
    external_url_info: ExternalUrlInfo,
    external_url: ExternalUrl = Depends(ExternalUrl),
):
    url_code = await external_url.generate_url(
        room_id=external_url_info.room_id,
        use_once_only=external_url_info.use_once_only,
    )
    return JSONResponse({"url_code": url_code})


@router.post("/replace-url")
async def replace_existing_url(url_code: str, external_url: ExternalUrl = Depends(ExternalUrl)):
    new_url_code = await external_url.replace_existing_url(url_code=url_code)
    return JSONResponse({"url_code": new_url_code})


@router.get("/i/{url_code}")
async def get_invite(
    request: Request, url_code: str, external_url: ExternalUrl = Depends(ExternalUrl)
):
    session_data = fastapi_sessions.get_session(request)

    is_invited = await external_url.get_room_invite(
        url_code=url_code,
        user_id=session_data.matrix_user,
    )
    if not is_invited:
        return RedirectResponse("/login")
    return RedirectResponse("/")
