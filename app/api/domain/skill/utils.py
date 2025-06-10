from fastapi import HTTPException
from .models import Skill
from db.crud.crud import CRUD


def get_skills_from_db(crud: CRUD, skill_info={}):
    filters = skill_info

    skills = crud.read_all(Skill)

    return skills


def get_skill_from_db(crud: CRUD, skill_info={}):
    filters = skill_info

    skills = crud.read(Skill, filters=filters)

    return skills


def add_skill_to_db(skill_data, crud: CRUD):

    crud.create(Skill(name=skill_data['name']))
