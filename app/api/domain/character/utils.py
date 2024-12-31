from fastapi import HTTPException
from .models import Character
from db.crud.crud import CRUD
from ..skill.models import Skill
from ..property.models import Property


def add_character_to_db(character_data, crud: CRUD):
    skills = [crud.read(Skill, skill_id) for skill_id in character_data['skills']]
    properties = [crud.read(Property, property_id) for property_id in character_data['properties']]

    crud.create(Character(
        name=character_data['name'],
        atk=character_data['atk'],
        hp=character_data['hp'],
        range=character_data['range'],
        skills=skills,
        properties=properties
    ))


def get_characters_from_db(crud: CRUD, character_info={}, skills=None, properties=None):
    filters = {key: value for key, value in character_info if value}

    if skills:
        filters.update(dict(skills=skills))
    if properties:
        filters.update(dict(properties=properties))
    characters = crud.read_all(Character, **filters)
    return characters


def get_character_from_db(character_id: int, crud: CRUD):
    db_character = crud.read(Character, character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_character


def update_character_from_db(character_id:int, character_data: dict, crud: CRUD):
    skills = [crud.read(Skill, skill_id) for skill_id in character_data['skills']]
    properties = [crud.read(Property, property_id) for property_id in character_data['properties']]

    db_character = crud.update(Character, character_id,
        name=character_data['name'],
        atk=character_data['atk'],
        hp=character_data['hp'],
        range=character_data['range'],
        skills=skills,
        properties=properties)
    if db_character is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_character


def delete_character_from_db(character_id: int, crud: CRUD):
    db_character = crud.delete(Character, character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_character