from ..character.utils import get_characters_from_db
from ..character.models import Character
from ..property.models import Property
from ..skill.models import Skill, Immunity
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
        limit=100
    )

def get_filtered_characters_by_property(enemy: Enemy, crud):
    # 1. 먼저 속성 기반 추천 캐릭터 리스트
    candidates = get_recommend_characters_by_property(enemy, crud)

    # 2. enemy의 immunity → 대응되는 skill name 리스트로 변환
    immunity_names = [imm.name for imm in enemy.immunities]

    # 면역 이름을 → 대응 스킬 이름으로 바꿔주는 매핑 함수 정의
    immunity_to_skill_map = {
        "날려버린다": "날려버린다",
        "멈춘다": "멈춘다",
        "느리게 한다": "느리게 한다",
        "워프": "워프",
        "고대의 저주": "고대의 저주",
        "독 공격": "독 공격",
        "공격력 다운": "공격력 다운",
        "폭파데미지": "폭파",
        "열파데미지": "열파",
        "파동데미지": "파동"
    }

    blocked_skills = {
        immunity_to_skill_map[imm] 
        for imm in immunity_names 
        if imm in immunity_to_skill_map
    }

    # 3. 캐릭터 중 blocked 스킬을 가진 애들 제외
    filtered = []
    for char in candidates:
        skill_names = {s.name for s in char.skills}
        if skill_names.isdisjoint(blocked_skills):  # 교집합 없음 → 포함
            filtered.append(char)

    return filtered

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

    if len(skill_objs) == 0:
        return []


    options = [joinedload(Character.skills)]
    return crud.list(
        Character,
        filters=None,
        where=[Character.skills.any(Skill.id == skill.id) for skill in skill_objs],
        options=options,
        limit=None
    )


def get_recommend_characters_by_immunity(enemy, crud):
    imm_queries = []
    for sk in enemy.skills:
        for cond in get_immunity_related_skills(sk.name) or []:
            imm_queries.append(cond)

    imm_objs = [
        crud.get(Immunity, filters=cond) 
        for cond in imm_queries
    ]

    if len(imm_objs) == 0:
        return []

    options = [joinedload(Character.immunities)]
    return crud.list(
        Character,
        filters=None,
        where=[Character.immunities.any(Immunity.id == imm.id) for imm in imm_objs],
        options=options,
        limit=None
    )

def get_skill_against(skill_name):
    list_by_skill = []
    if skill_name in ["파동", "소파동"]:
        list_by_skill.append({"name": "파동 삭제"})
    if skill_name in ["열파", "소열파"]:
        list_by_skill.append({"name": "열파반사"}) 
    if skill_name == "베리어":
        list_by_skill.append({"name": "베리어 브레이커"})
    if skill_name == "쉴드":
        list_by_skill.append({"name": "쉴드 브레이커"})
    return list_by_skill


def get_skill_related_properties(property_name):
    list_by_property = []
    if property_name == "좀비":
        list_by_property.append({"name": f"{property_name}킬러"})
        list_by_property.append({"name": "영혼 공격"})
    if property_name == "메탈":
        list_by_property.append({"name": "크리티컬"})
        list_by_property.append({"name": f"{property_name}킬러"})
    return list_by_property


def get_immunity_related_skills(skill_name):
    list_by_skill = []
    if skill_name in ["멈춘다", "공격력 다운", "독 공격", "밀치기", "고대의 저주", "워프", "느리게 한다"]:
        list_by_skill.append({"name": f"{skill_name}"})
    if skill_name in ["파동", "소파동"]:
        list_by_skill.append({"name": "파동데미지"})
    if skill_name in ["열파", "소열파", "순교", "열파반사"]:
        list_by_skill.append({"name": "열파데미지"}) 
    if skill_name == "폭파":
        list_by_skill.append({"name": "폭파데미지"})
    return list_by_skill


def make_prompt(enemy, recommendations: list[dict]) -> str:
    prompt = f"아래는 게임에서 적과 그에 대응하는 추천 캐릭터 목록입니다.\n"
    prompt += f"이 정보를 바탕으로 유저에게 추천 캐릭터들을 **자연스럽고 친절하게** 설명해주세요.\n\n"

    prompt += f"### 🧟 적 정보\n"
    prompt += f"- 이름: {enemy.name}\n"
    prompt += f"- 사정거리: {enemy.range} 이상\n"
    prompt += f"- 속성: {', '.join([p.name for p in enemy.properties]) if enemy.properties else '없음'}\n"
    prompt += f"- 특수능력: {', '.join([s.name for s in enemy.skills]) if enemy.skills else '없음'}\n"
    prompt += f"- 내성: {', '.join([i.name for i in enemy.immunities]) if enemy.immunities else '없음'}\n\n"

    prompt += f"### 🧙 추천 캐릭터\n"

    for rec in recommendations:
        names = rec["character_names"]
        explanations = rec["explanations"]
        prompt += f"- `{rec['base_id']}` 기준 캐릭터:\n"
        for name, reason in zip(names, explanations):
            prompt += f"    - {name}: {reason}\n"
        prompt += "\n"

    prompt += "위 내용을 바탕으로 어떤 캐릭터가 어떤 이유로 추천되는지, 초보 유저도 이해할 수 있도록 부드럽고 자연스럽게 설명해줘.\n"

    return prompt