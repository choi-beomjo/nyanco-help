from ..character.utils import get_characters_from_db
from ..character.models import Character
from ..property.models import Property
from ..skill.models import Skill
from ..enemy.models import Enemy
from sqlalchemy.orm import joinedload

def get_recommend_characters_by_property(enemy: Enemy, crud):

    prop_objs = [
        prop.id
        for prop in enemy.properties
    ]
    # eager load 관계
    options = [joinedload(Character.properties)]
    return crud.list(
        Character,
        filters=None,
        where=[Character.properties.any(Property.id == prop_id) for prop_id in prop_objs],
        options=options,
    )


def get_recommend_characters_by_range(enemy, crud):
    
    return crud.read_all(
        model=Character,
        custom_conditions=[Character.range > enemy.range]  # 사용자 정의 조건
    )


def get_recommend_characters_by_skills(enemy, crud):
    # 1) 속성·스킬 기반 필터 조건 생성
    skill_queries = []
    for sk in enemy.skills:
        for cond in get_skill_against(sk.name) or []:
            skill_queries.append(cond)
    for prop in enemy.properties:
        for cond in get_skill_related_properties(prop.name) or []:
            skill_queries.append(cond)

    # 2) Skill 객체 리스트로 치환
    skill_objs = [
        crud.get(Skill, filters=cond) 
        for cond in skill_queries
    ]
    options = [joinedload(Character.skills)]
    return crud.list(
        Character,
        filters=None,
        where=[Character.skills.any(Skill.id == skill_id) for skill_id in skill_objs],
        options=options,
    )


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
