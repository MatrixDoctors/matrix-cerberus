from fastapi import FastAPI, Depends
from starlette.requests import Request

from app.api.routers import users

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi")

@app.get("/api")
async def root():
    return {"message": "Hello World"}

# Routers
app.include_router(
    users.router,
    prefix="/api/users",
    tags=["users"],
)