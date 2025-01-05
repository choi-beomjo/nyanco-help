from ..character.utils import get_characters_from_db
from ..character.models import Character


def get_recommend_characters_by_property(enemy_info: dict, crud):

    property_ids = [prop.id for prop in enemy_info.properties]

    characters = get_characters_from_db(crud=crud, properties=property_ids)
    return characters


def get_recommend_characters_by_range(enemy, crud):
    
    return crud.read_all(
        model=Character,
        custom_conditions=[Character.range > enemy.range]  # 사용자 정의 조건
    )