from fastapi import APIRouter

from .board.api import router


api = APIRouter()
api.include_router(router)