from fastapi import HTTPException
from .models import Enemy
from db.crud.crud import CRUD
from ..skill.models import Skill
from ..property.models import Property
from sqlalchemy.orm import joinedload

def add_enemy_to_db(enemy_data, crud: CRUD):
    enemy_data['skills'] = [crud.get(Skill, obj_id=sid) for sid in enemy_data['skills']]
    enemy_data['properties'] = [crud.get(Property, obj_id=pid) for pid in enemy_data['properties']]
    crud.create(Enemy(**enemy_data))



def get_enemies_from_db(crud: CRUD, enemy_info={}, skills=None, properties=None, skip=0, limit=None):
    filters = {key: value for key, value in enemy_info if value}

    skill_objs = [crud.get(Skill, obj_id=sid) for sid in skills] if skills else []
    prop_objs  = [crud.get(Property, obj_id=pid) for pid in properties] if properties else []

    if skill_objs:
        filters["skills"] = skill_objs
    if prop_objs:
        filters["properties"] = prop_objs

    options = []
    if skill_objs:
        options.append(joinedload(Enemy.skills))
    if prop_objs:
        options.append(joinedload(Enemy.properties))

    enemies = crud.list(Enemy, filters=filters, options=options, skip=skip, limit=limit)
    return enemies


def get_enemy_from_db(enemy_id: int, crud: CRUD):
    db_enemy = crud.get(Enemy, obj_id=enemy_id, options=[joinedload(Enemy.skills), joinedload(Enemy.properties)])
    if db_enemy is None:
        raise HTTPException(status_code=404, detail=f"Enemy not found: {enemy_id}")
    return db_enemy


def get_duplicate_enemy(enemy_info: dict, crud: CRUD):
    return crud.read(Enemy, enemy_info)


def update_enemy_from_db(enemy_id:int, enemy_data: dict, crud: CRUD):
    enemy_data['skills'] = [crud.get(Skill, obj_id=sid) for sid in enemy_data['skills']]
    enemy_data['properties'] = [crud.get(Property, obj_id=pid) for pid in enemy_data['properties']]

    db_enemy = crud.update(Enemy, enemy_id, **enemy_data)
    if db_enemy is None:
        raise HTTPException(status_code=404, detail=f"Enemy not found: {enemy_id}")
    return db_enemy


def delete_enemy_from_db(enemy_id: int, crud: CRUD):
    db_enemy = crud.delete(Enemy, enemy_id)
    if db_enemy is None:
        raise HTTPException(status_code=404, detail=f"Enemy not found: {enemy_id}")
    return db_enemy