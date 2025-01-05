from ..character.utils import get_characters_from_db


def get_recommend_characters_by_property(enemy_info: dict, crud):

    property_ids = [prop.id for prop in enemy_info.properties]
    #properties = [key for key, value in enemy_info['properties']]
    characters = get_characters_from_db(crud=crud, properties=property_ids)
    return characters