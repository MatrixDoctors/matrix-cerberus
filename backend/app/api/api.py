from fastapi import APIRouter, Depends

from app.api.endpoints import external_url, users
from app.matrix.external_url import ExternalUrl

api_router = APIRouter()

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)

api_router.include_router(
    external_url.router,
    prefix="/external-url",
    tags=["external url"],
    dependencies=[Depends(ExternalUrl)],
)
