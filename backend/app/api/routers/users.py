from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

router = APIRouter()

@router.get("/")
async def message_users():
    return {"message": "Hello User!!!"}