from fastapi import APIRouter, Depends
from ...tags import Tags
from utils.msg.msg import Msg
from ...deps import get_current_user, get_crud, CRUD, admin_required
from ..enemy.utils import get_enemy_from_db, get_enemies_from_db
from .utils import *
from ..character.schemas import CharacterInfo
from ..character.models import Character


router = APIRouter(tags=[Tags.recommend])


@router.get('/{enemy_id}')
async def get_characters_by_property(enemy_id: int, crud: CRUD=Depends(get_crud)):
    enemy = get_enemy_from_db(enemy_id=enemy_id, crud=crud)
    
    characters = get_recommend_characters_by_property(enemy_info=enemy, crud=crud)
    characters_by_range = get_recommend_characters_by_range(enemy, crud)
    return { 
        "characters_by_properties": [CharacterInfo.from_orm(character) for character in characters],
        "characters_by_range": [CharacterInfo.from_orm(character) for character in characters_by_range]
    }
    
