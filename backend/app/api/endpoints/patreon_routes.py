from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/login")
async def get_login():
    return JSONResponse({"msg": "success"})
