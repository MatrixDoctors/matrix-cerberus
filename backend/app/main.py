from fastapi import Depends, FastAPI

from app.api import api
from app.core.background_runner import matrix_bot_runner

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi")

@app.on_event('startup')
async def app_startup():
    matrix_bot_runner.create_background_task()

@app.on_event('shutdown')
async def app_shutdown():
    await matrix_bot_runner.cancel_background_task()

@app.get("/api")
async def root():
    return {"message": "Hello World"}


# Endpoints
app.include_router(
    api.api_router,
    prefix="/api",
)
