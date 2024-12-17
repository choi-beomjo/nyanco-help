from fastapi import APIRouter, Depends
from ...tags import Tags
from utils.msg.msg import Msg
from .utils import *
from .schemas import *
from .models import *
from ...deps import get_current_user, get_crud, CRUD

router = APIRouter(tags=[Tags.enemy])


@router.get("/list", response_model=List[EnemyInfo])
def get_enemy_list(crud: CRUD = Depends(get_crud)):
    enemies = get_enemies_from_db(crud=crud)
    return [EnemyInfo.from_orm(enemy) for enemy in enemies]



@router.post("")
def post_enemy(enemy_info: EnemyInfo, crud: CRUD = Depends(get_crud)):
    
    enemy_data = enemy_info.dict()
    add_enemy_to_db(enemy_data=enemy_data, crud=crud)

    return Msg(msg="success")


@router.get("/{enemy_id}")
def get_enemy(enemy_id: int, crud: CRUD = Depends(get_crud)):
    return