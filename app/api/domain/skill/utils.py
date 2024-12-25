from fastapi import HTTPException
from .models import Skill
from db.crud.crud import CRUD


def get_skills_from_db(crud: CRUD, skill_info={}):
    filters = {key: value for key, value in skill_info if value}

    skills = crud.read_all(Skill)

    return skills