from fastapi import HTTPException
from .models import Character
from db.crud.crud import CRUD
from ..skill.models import Skill
from ..property.models import Property
from sqlalchemy.orm import joinedload


def add_character_to_db(character_data, crud: CRUD):
    character_data['skills'] = [crud.get(Skill, obj_id=skill_id) for skill_id in character_data['skills']]
    character_data['properties'] = [crud.get(Property, obj_id=property_id) for property_id in character_data['properties']]
    crud.create(Character(**character_data))



def get_characters_from_db(crud: CRUD, character_info={}, skills=None, properties=None, skip=0, limit=None):
    # 1) 기본 필터 생성
    filters = {
        key: value
        for key, value in (character_info or {}).items()
        if value is not None
    }

    # 2) Skill / Property 객체로 변환
    skill_objs = [crud.get(Skill, obj_id=sid) for sid in skills] if skills else []
    prop_objs  = [crud.get(Property, obj_id=pid) for pid in properties] if properties else []

    if skill_objs:
        filters["skills"] = skill_objs
    if prop_objs:
        filters["properties"] = prop_objs

    # 3) 관계를 미리 로드할 옵션 지정
    options = []
    if skill_objs:
        options.append(joinedload(Character.skills))
    if prop_objs:
        options.append(joinedload(Character.properties))

    # 4) 리스트 조회 (skip과 limit 파라미터 추가)
    return crud.list(
        Character,
        filters=filters,
        options=options,
        skip=skip,
        limit=limit,
    )


def get_duplicate_character(character_info: dict, crud: CRUD):
    return crud.read(Character, character_info)


def get_character_from_db(character_id: int, crud: CRUD):
    db_character = crud.get(Character, obj_id=character_id, options=[joinedload(Character.skills), joinedload(Character.properties)])
    if db_character is None:
        raise HTTPException(status_code=404, detail=f"Character not found: {character_id}")
    return db_character


def update_character_from_db(character_id:int, character_data: dict, crud: CRUD):
    
    character_data['skills'] = [crud.read(Skill, skill_id) for skill_id in character_data['skills']]
    character_data['properties'] = [crud.read(Property, property_id) for property_id in character_data['properties']]

    db_character = crud.update(Character, character_id, **character_data)
    if db_character is None:
        raise HTTPException(status_code=404, detail=f"Character not found: {character_id}")
    return db_character


def delete_character_from_db(character_id: int, crud: CRUD):
    db_character = crud.delete(Character, character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail=f"Character not found: {character_id}")
    return db_character