from fastapi import APIRouter, Depends
from ...tags import Tags
from utils.msg.msg import Msg
from ...deps import get_current_user, get_crud, CRUD, admin_required
from ..enemy.utils import get_enemy_from_db, get_enemies_from_db
from .utils import *
from ..character.schemas import CharacterInfo


router = APIRouter(tags=[Tags.recommend])


@router.get('/{enemy_id}')
async def get_characters_by_property(enemy_id: int, crud: CRUD=Depends(get_crud)):
    enemy = get_enemy_from_db(enemy_id=enemy_id, crud=crud)
    
    characters = get_recommend_characters_by_property(enemy_info=enemy, crud=crud)

    return [CharacterInfo.from_orm(character) for character in characters]
    
