from fastapi import APIRouter

from .domain.board.api import router as board_router
from .domain.user.api import router as user_router

api = APIRouter()
api.include_router(board_router, prefix="/board")
api.include_router(user_router, prefix="/user")