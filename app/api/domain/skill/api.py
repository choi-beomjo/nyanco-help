from fastapi import APIRouter, Depends
from ...tags import Tags
from utils.msg.msg import Msg
from .utils import *
from .schemas import *
from ...deps import get_current_user, get_crud, CRUD, admin_required


router = APIRouter(tags=[Tags.skill])


@router.get("/list")
def get_skill_list(crud: CRUD = Depends(get_crud)):
    skills = get_skills_from_db(crud=crud)
    return [SkillInfo.from_orm(skill) for skill in skills]


@router.post("")
def post_enemy(skill_info: SkillPost, crud: CRUD = Depends(get_crud), current_user=Depends(admin_required)):
    
    skill_data = skill_info.dict()
    add_skill_to_db(enemy_data=skill_data, crud=crud)

    return Msg(msg="success")