from ..character.utils import get_characters_from_db
from ..character.models import Character
from ..skill.models import Skill


def get_recommend_characters_by_property(enemy_info: dict, crud):

    property_ids = [prop.id for prop in enemy_info.properties]

    characters = get_characters_from_db(crud=crud, properties=property_ids)
    return characters


def get_recommend_characters_by_range(enemy, crud):
    
    return crud.read_all(
        model=Character,
        custom_conditions=[Character.range > enemy.range]  # 사용자 정의 조건
    )


def get_recommend_characters_by_skills(enemy, crud):
    filters = dict(skills=[crud.read(Skill, get_skill_against(skill.name)) for skill in enemy.skills])
    characters = crud.read_all(Character, **filters)
    return characters


def get_skill_against(skill_name):
    if skill_name in ["멈추기", "공격력 다운", "독 데미지", "날려버린다", "파동", "고대의 저주"]:
        return {"name": f"{skill_name} 무효"}
    elif skill_name == "파동":
        return {"name": f"{skill_name} 무효" }
    return None
    