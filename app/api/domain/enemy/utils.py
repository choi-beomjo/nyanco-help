from fastapi import HTTPException
from .models import Enemy, Skill, Property
from db.crud.crud import CRUD


def add_enemy_to_db(enemy_data, crud: CRUD):
    skills = crud.read_all(Skill, name=enemy_data['skills'][0])
    properties = crud.read_all(Property, name=enemy_data['properties'][0])

    crud.create(Enemy(
        **enemy_data,
        #atk=enemy_info.atk,
        #hp=enemy_info.hp,
        #range=enemy_info.range,
        skills=skills,
        properties=properties
    ))