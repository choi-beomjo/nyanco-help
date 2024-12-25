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