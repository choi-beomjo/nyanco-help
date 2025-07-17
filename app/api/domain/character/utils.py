from fastapi import HTTPException
from .models import Character, CharacterInstinct
from db.crud.crud import CRUD
from ..skill.models import Skill
from ..property.models import Property
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, or_


def add_character_to_db(character_data, crud: CRUD):
    character_data['skills'] = [crud.get(Skill, obj_id=skill_id) for skill_id in character_data['skills']]
    character_data['properties'] = [crud.get(Property, obj_id=property_id) for property_id in character_data['properties']]
    crud.create(Character(**character_data))


def get_characters_from_db(crud: CRUD, character_info={}, like_filters={}, skills=None, properties=None, skip=0, limit=None):
    # 1) 기본 필터 생성
    filters = {
        key: value
        for key, value in (character_info or {}).items()
        if value is not None
    }

    # 2) 관계를 미리 로드할 옵션 지정
    options = []
    if skills:
        options.append(joinedload(Character.skills))
    if properties:
        options.append(joinedload(Character.properties))

    # 3) 관계 필터링 조건 생성
    where_conditions = get_where_conditions(skills, properties)

    # 4) 리스트 조회 (where 조건 사용)
    characters = crud.list(
        Character,
        filters=filters,
        like_filters=like_filters or {},
        where=where_conditions,
        options=options,
        skip=skip,
        limit=limit,
    )
    
    # 5) 각 캐릭터에 instincts 로드
    for character in characters:
        character.instincts = get_instincts_from_db(crud, base_id=character.base_id)
    
    return characters


def get_duplicate_character(character_info: dict, crud: CRUD):
    return crud.read(Character, character_info)


def get_character_from_db(character_id: int, crud: CRUD):
    db_character = crud.get(Character, obj_id=character_id, options=[joinedload(Character.skills), joinedload(Character.properties)])
    if db_character is None:
        raise HTTPException(status_code=404, detail=f"Character not found: {character_id}")
    
    # instincts 로드 (base_id 기준으로)
    db_character.instincts = get_instincts_from_db(crud, base_id=db_character.base_id)
    
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


def count_characters_from_db(crud: CRUD, character_info={}, skills=None, properties=None):
    """
    조건에 맞는 캐릭터 수를 반환
    """
    # 1) 기본 필터 생성
    filters = {
        key: value
        for key, value in (character_info or {}).items()
        if value is not None
    }

    # 2) 관계 필터링 조건 생성
    where_conditions = get_where_conditions(skills, properties)

    # 3) 카운트 조회
    return crud.count(Character, filters=filters, where=where_conditions)


def get_where_conditions(skills, properties):
    where_conditions = []
    if skills:
        skill_ids = [skill for skill in skills]
        where_conditions.append(Character.skills.any(Skill.id.in_(skill_ids)))
    if properties:
        prop_ids = [prop for prop in properties]
        where_conditions.append(Character.properties.any(Property.id.in_(prop_ids)))
    return where_conditions


def get_instincts_from_db(crud: CRUD, base_id=None):
    from sqlalchemy.orm import joinedload
    return crud.list(
        CharacterInstinct, 
        filters={'base_id': base_id},
        options=[joinedload(CharacterInstinct.instinct)]
    )