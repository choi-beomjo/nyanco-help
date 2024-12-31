from fastapi import APIRouter

from .domain.board.api import router as board_router
from .domain.user.api import router as user_router
from .domain.enemy.api import router as enemy_router
from .domain.skill.api import router as skill_router
from .domain.property.api import router as property_router
from .domain.character.api import router as character_router

api = APIRouter()
api.include_router(board_router, prefix="/board")
api.include_router(user_router, prefix="/user")
api.include_router(character_router, prefix="/character")
api.include_router(enemy_router, prefix="/enemy")
api.include_router(skill_router, prefix="/skill")
api.include_router(property_router, prefix="/property")