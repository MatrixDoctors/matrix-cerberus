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
    global background_validator

    await app_state.setup_state()
    await app_state.matrix_bot_runner.initialise_bot()
    await app_state.start_session()
    background_validator = BackgroundValidater(
        bot_client=app_state.bot_client,
        http_client=app_state.http_client,
        github_default_role=app_state.settings.github.organisation_membership,
    )
    await background_validator.create_background_task()


@app.on_event("shutdown")
async def app_shutdown():
    global background_validator

    await background_validator.cancel_background_task()
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
