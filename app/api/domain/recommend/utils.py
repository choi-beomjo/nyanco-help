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
    # 스킬 기반 필터 
    skill_filters = [
        crud.read(Skill, condition)
        for skill in enemy.skills
        for condition in (get_skill_against(skill.name) or [])
    ]
    
    # 속성 기반 필터 추가
    property_filters = [
        crud.read(Skill, condition)
        for property in enemy.properties
        for condition in (get_skill_related_properties(property.name) or [])
    ]

    # 모든 필터 합치기
    filters = {"skills": skill_filters + property_filters}

    # 캐릭터 검색
    characters = crud.read_all(Character, **filters)
    return characters


def get_skill_against(skill_name):
    if skill_name == "파동":
        return [{"name": "파동 무효"}, {"name": "파동 삭제"}]
    elif skill_name in ["멈추기", "공격력 다운", "독 데미지", "날려버린다", "고대의 저주"]:
        return [{"name": f"{skill_name} 무효"}]
    return None


def get_skill_related_properties(property_name):
    if property_name == "좀비":
        return [{"name": f"{property_name} 킬러"}]
    elif property_name == "메탈":
        return [{"name": "크리티컬"}, {"name": f"{property_name} 킬러"}]
    return None
