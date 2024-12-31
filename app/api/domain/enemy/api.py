from fastapi import APIRouter, Depends
from ...tags import Tags
from utils.msg.msg import Msg
from .utils import *
from .schemas import *
from .models import *
from ...deps import get_current_user, get_crud, CRUD, admin_required
from ..skill.schemas import SkillInfo


router = APIRouter(tags=[Tags.enemy])


@router.get("/list")
def get_enemy_list(crud: CRUD = Depends(get_crud)):
    enemies = get_enemies_from_db(crud=crud)
    return [EnemyInfo.from_orm(enemy) for enemy in enemies]


@router.post("")
def post_enemy(enemy_info: EnemyData, crud: CRUD = Depends(get_crud), current_user=Depends(admin_required)):
    
    enemy_data = enemy_info.dict()
    add_enemy_to_db(enemy_data=enemy_data, crud=crud)

    return Msg(msg="success")


@router.get("/{enemy_id}")
def get_enemy(enemy_id: int, crud: CRUD = Depends(get_crud)):
    enemy = get_enemy_from_db(enemy_id=enemy_id, crud=crud)
    return EnemyInfo.from_orm(enemy)


@router.put("/{enemy_id}")
def update_enemy(enemy_info: EnemyData, enemy_id: int, crud: CRUD = Depends(get_crud), current_user=Depends(admin_required)):
    enemy = update_enemy_from_db(enemy_id=enemy_id, enemy_data=enemy_info.dict(), crud=crud)
    return EnemyInfo.from_orm(enemy)


@router.delete("/{enemy_id}")
def delete_enemy(enemy_id: int, crud: CRUD = Depends(get_crud), current_user=Depends(admin_required)):
    enemy = delete_enemy_from_db(enemy_id=enemy_id, crud=crud)
    return Msg(msg="sucess")