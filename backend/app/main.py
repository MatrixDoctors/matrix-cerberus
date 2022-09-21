from fastapi import Depends, FastAPI

from app.api import api
from app.core.app_state import app_state
from app.matrix.background_validator import BackgroundValidater

# from app.core.background_runner import matrix_bot_runner

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi")

background_validator = None


@app.on_event("startup")
async def app_startup():
    # Fetch the initial sync from matrix homeserver
    await app_state.setup_state()
    await app_state.start_session()


@app.on_event("shutdown")
async def app_shutdown():
    await app_state.close_session()
    await app_state.delete_state()


@app.get("/api")
async def root():
    return {"message": "Hello World"}


# Endpoints
app.include_router(
    api.api_router,
    prefix="/api",
)
