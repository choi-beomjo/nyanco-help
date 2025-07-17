from fastapi import APIRouter, Depends
from ...tags import Tags
from utils.msg.msg import Msg
#from .utils import *
from .schemas import *
from ..enemy.models import Enemy
from .models import *
from ...deps import get_current_user, get_crud, CRUD, admin_required
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
router = APIRouter()

@router.get("/list", response_model=StageList, tags=[Tags.stage])
def get_stage_list(
    page: int = 1,
    page_size: int = 10,
    crud: CRUD = Depends(get_crud)):

    stages = crud.list(Stage, options=[joinedload(Stage.enemies)], skip=(page-1)*page_size, limit=page_size)
    total = crud.count(Stage)
   
    return StageList(
        data=[StageInfo.from_orm(stage) for stage in stages],
        total=total,
        page=page,
        page_size=page_size
    )



@router.post("", tags=[Tags.stage])
def post_stage(req: StageInfo, crud: CRUD = Depends(get_crud)):
    stage_info = req.dict()

    crud.create(Stage(**stage_info))


@router.get("/{stage_id}", response_model=StageInfo, tags=[Tags.stage])
def get_stage_with_enemies(stage_id: str, crud: CRUD = Depends(get_crud)):
    stage = crud.get(Stage, obj_id=stage_id, options=[joinedload(Stage.enemies)])

    if not stage:
        raise HTTPException(status_code=404, detail=f"Stage not found: {stage_id}")

    return StageInfo.from_orm(stage)




@router.post("/{stage_id}/enemy", tags=[Tags.stage])
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



@router.get("/search/name", tags=[Tags.stage])
def search_stages_from_enemies(name: str, page: int = 1, page_size: int = 10, crud: CRUD=Depends(get_crud)):
    # stage name으로 검색
    stages = crud.list(Stage, like_filters=dict(name=name), options=[joinedload(Stage.enemies)], skip=(page-1)*page_size, limit=page_size)
    total = crud.count(Stage, like_filters=dict(name=name))
    
    return StageList(
        data=[StageInfo.from_orm(stage) for stage in stages],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{enemy_id}/stage", tags=[Tags.stage])
def search_stages_from_enemies(enemy_id: int, crud: CRUD=Depends(get_crud)):
    
    return crud.read(Enemy, filters=dict(id=enemy_id), relationships=["stages"])