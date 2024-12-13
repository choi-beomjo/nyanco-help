from fastapi import APIRouter, Depends
from ...tags import Tags
from .utils import *
from .schemas import *
from ...deps import get_current_user, get_crud, CRUD

router = APIRouter(tags=[Tags.enemy])


@router.get("/list")
def get_enemy_list(crud: CRUD = Depends(get_crud)):
    return 