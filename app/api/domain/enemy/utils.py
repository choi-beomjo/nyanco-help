from fastapi import HTTPException
from .models import Enemy, Skill, Property
from db.crud.crud import CRUD


def add_enemy_to_db(enemy_data, crud: CRUD):
    skills = [crud.read_all(Skill, name=skill)[0] for skill in enemy_data['skills']]
    properties = [crud.read_all(Property, name=property)[0] for property in enemy_data['properties']]

    crud.create(Enemy(
        atk=enemy_data['atk'],
        hp=enemy_data['hp'],
        range=enemy_data['range'],
        skills=skills,
        properties=properties
    ))


def get_enemies_from_db(crud: CRUD, enemy_info={}, skills=None, properties=None):
    filters = {key: value for key, value in enemy_info if value}

    if skills:
        filters.update(dict(skills=skills))
    if properties:
        filters.update(dict(properties=properties))
    enemies = crud.read_all(Enemy, **filters)
    return enemies