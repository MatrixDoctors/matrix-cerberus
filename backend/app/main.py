from fastapi import Depends, FastAPI

from app.api import api
from app.core.global_app_state import app_state

# from app.core.background_runner import matrix_bot_runner

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi")


@app.on_event("startup")
async def app_startup():
    await app_state.setup_state()


@app.on_event("shutdown")
async def app_shutdown():
    await app_state.close()


@app.get("/api")
async def root():
    return {"message": "Hello World"}


# Endpoints
app.include_router(
    api.api_router,
    prefix="/api",
)
