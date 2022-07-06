from fastapi import Depends, FastAPI

from app.api import api
from app.core.global_app_state import app_state
from app.core.http_client import http_client

# from app.core.background_runner import matrix_bot_runner

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi")


@app.on_event("startup")
async def app_startup():
    await http_client.start_session()
    # matrix_bot_runner.create_background_task()
    await app_state.setup_state()


@app.on_event("shutdown")
async def app_shutdown():
    await http_client.stop_session()
    # await matrix_bot_runner.cancel_background_task()
    await app_state.close()


@app.get("/api")
async def root():
    return {"message": "Hello World"}


# Endpoints
app.include_router(
    api.api_router,
    prefix="/api",
)
