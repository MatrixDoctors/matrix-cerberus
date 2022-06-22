from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.api.deps import fastapi_sessions
from app.api.models import ExternalUrlInfo
from app.matrix.external_url import ExternalUrl

router = APIRouter()


@router.post("/generate-url")
async def generate_url(
    request: Request,
    external_url_info: ExternalUrlInfo,
    external_url: ExternalUrl = Depends(ExternalUrl),
):
    session_data = fastapi_sessions.get_session(request)
    url_code = await external_url.generate_url(
        matrix_homeserver=session_data.matrix_homeserver,
        room_id=external_url_info.room_id,
        use_once_only=external_url_info.use_once_only,
    )
    return JSONResponse({"url_code": url_code})
