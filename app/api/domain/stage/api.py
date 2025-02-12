from fastapi import APIRouter, Depends
from ...tags import Tags
from utils.msg.msg import Msg
#from .utils import *
from .schemas import *
from ..enemy.models import Enemy
from .models import *
from ...deps import get_current_user, get_crud, CRUD, admin_required


router = APIRouter()

@router.get("")
def get_stage_list(crud: CRUD = Depends(get_crud)):
    stages = crud.join_read(Stage)
    return [StageInfo.from_orm(stage) for stage in stages]



@router.post("")
def post_stage(req: StageInfo, crud: CRUD = Depends(get_crud)):
    stage_info = req.dict()

    crud.create(Stage(**stage_info))


@router.get("/{stage_id}")
def get_stage_with_enemies(stage_id: int, crud: CRUD = Depends(get_crud)):
    stage = crud.read(
        model=Stage,
        filters=dict(id=stage_id),
        relationships=["enemies"]
    )
    stage = stage.__dict__
    enemies = [crud.read(Enemy, filters=dict(id=enemy.__dict__["enemy_id"])) for enemy in stage["enemies"]]
    return StageInfo(name=stage["name"], enemies=enemies)



@router.post("/{stage_id}")
def add_enemy_to_stage(stage_id: int, enemy_id: int, crud: CRUD = Depends(get_crud)):
    
    enemy = crud.read(Enemy, filters=dict(id=enemy_id), single=True)
    stage = crud.read(Stage, filters=dict(id=stage_id), single=True)

    enemy_stage = crud.read(StageEnemy, filters=dict(stage_id=stage_id, enemy_id=enemy_id), single=True)
    
    if not enemy:
        return {"message": "Enemy not found", "status": 400}
    if not stage:
        return {"message": "Stage not found", "status": 400}
    
    if enemy_stage:
        return {"message": "Enemy is already in this stage", "status": 200}


    new_enemy_stage = crud.create(StageEnemy(stage_id=stage_id, enemy_id=enemy_id))
    return {"message": "Enemy added to stage successfully", "status": 201, "data": new_enemy_stage}



@router.post("/search")
def search_stages_from_enemies():
    pass