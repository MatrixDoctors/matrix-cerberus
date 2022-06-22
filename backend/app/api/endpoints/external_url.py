from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.background_runner import matrix_bot_runner
from app.core.http_client import http_client

router = APIRouter()
