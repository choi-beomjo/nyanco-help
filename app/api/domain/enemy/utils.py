from fastapi import HTTPException
from .models import Enemy
from db.crud.crud import CRUD
from ..skill.models import Skill
from ..property.models import Property


def add_enemy_to_db(enemy_data, crud: CRUD):
    skills = [crud.read(Skill, skill_id) for skill_id in enemy_data['skills']]
    properties = [crud.read(Property, property_id) for property_id in enemy_data['properties']]

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


def get_enemy_from_db(enemy_id: int, crud: CRUD):
    db_enemy = crud.read(Enemy, enemy_id)
    if db_enemy is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_enemy


def update_enemy_from_db(enemy_id:int, enemy_data: dict, crud: CRUD):
    skills = [crud.read(Skill, skill_id) for skill_id in enemy_data['skills']]
    properties = [crud.read(Property, property_id) for property_id in enemy_data['properties']]

    db_enemy = crud.update(Enemy, enemy_id, atk=enemy_data['atk'],
        hp=enemy_data['hp'],
        range=enemy_data['range'],
        skills=skills,
        properties=properties)
    if db_enemy is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_enemy


def delete_enemy_from_db(enemy_id: int, crud: CRUD):
    db_enemy = crud.delete(Enemy, enemy_id)
    if db_enemy is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_enemy