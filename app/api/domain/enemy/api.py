from fastapi import APIRouter, Depends
from ...tags import Tags
from .utils import *
from .schemas import *
from .models import *
from ...deps import get_current_user, get_crud, CRUD

router = APIRouter(tags=[Tags.enemy])


@router.get("/list")
def get_enemy_list(crud: CRUD = Depends(get_crud)):
    #enemies = get_enemy_list_from_db(crud=crud)
    return 



@router.post("")
def post_enemy(enemy_info: EnemyInfo, crud: CRUD = Depends(get_crud)):
    
    enemy_data = enemy_info.dict()
    add_enemy_to_db(enemy_data=enemy_data, crud=crud)
    #skills = crud.read_all(Skill, name=enemy_data['skills'][0])
    #properties = crud.read_all(Property, name=enemy_data['properties'][0])

    #crud.create(Enemy(
    #    atk=enemy_info.atk,
    #    hp=enemy_info.hp,
    #    range=enemy_info.range,
    #    skills=skills,
    #    properties=properties
    #))
    return 