from fastapi import APIRouter, Depends
from ...tags import Tags
from utils.msg.msg import Msg
from ...deps import get_current_user, get_crud, CRUD, admin_required
from ..enemy.utils import get_enemy_from_db, get_enemies_from_db
from .utils import *
from .schemas import UserExperienceData
from .models import UserExperience
from ..character.schemas import CharacterInfo
import aiohttp
from google import genai
import os
from google.genai import types
# from utils.infer.set_model import *
# from .inference import recommend_characters


router = APIRouter(tags=[Tags.recommend])





@router.get('/{enemy_id}')
async def get_characters_by_property(enemy_id: int, crud: CRUD = Depends(get_crud)):
    from collections import defaultdict

    enemy = get_enemy_from_db(enemy_id=enemy_id, crud=crud)

    # 추천 기준별 캐릭터
    property_chars = get_filtered_characters_by_property(enemy, crud)
    range_chars = get_recommend_characters_by_range(enemy, crud)
    skill_chars = get_recommend_characters_by_skills(enemy, crud)
    immunity_chars = get_recommend_characters_by_immunity(enemy, crud)

    # 캐릭터별 matched_criteria 수집
    character_tag_map = {}
    criteria_sources = {
        "property": property_chars,
        "range": range_chars,
        "skill": skill_chars,
        "immunity": immunity_chars
    }

    for criterion, char_list in criteria_sources.items():
        for c in char_list:
            if c.id not in character_tag_map:
                character_tag_map[c.id] = {
                    "character": c,
                    "matched_criteria": set()
                }
            character_tag_map[c.id]["matched_criteria"].add(criterion)

    # base_id 기준 그룹핑
    grouped_by_base = defaultdict(list)
    for rec in character_tag_map.values():
        base_id = rec["character"].base_id
        grouped_by_base[base_id].append(rec)

    def get_explanation(matched_criteria):
        parts = []
        if "property" in matched_criteria:
            parts.append("속성 상성이 유리함")
        if "skill" in matched_criteria:
            parts.append("적의 주요 스킬에 대응 가능")
        if "immunity" in matched_criteria:
            parts.append("적의 스킬에 무력화되지 않음")
        if "range" in matched_criteria:
            parts.append("사거리가 길어 선공 가능")
        return " / ".join(parts)

    # base_id 단위 추천 정리
    recommendations = []
    for base_id, group in grouped_by_base.items():
        sorted_group = sorted(group, key=lambda x: (len(x["matched_criteria"]), x["character"].id), reverse=True)
        character_ids = [rec["character"].id for rec in sorted_group]
        character_names = [rec["character"].name for rec in sorted_group]
        matched_criteria = [list(rec["matched_criteria"]) for rec in sorted_group]
        explanations = [get_explanation(rec["matched_criteria"]) for rec in sorted_group]
        representative_id = sorted_group[0]["character"].id

        recommendations.append({
            "base_id": base_id,
            "character_ids": character_ids,
            "character_names": character_names,
            "matched_criteria": matched_criteria,
            "explanations": explanations,
            "representative_id": representative_id
        })

    # 필요 시 Top-N 제한 가능
    recommendations = sorted(recommendations, key=lambda x: len(x["matched_criteria"][-1]), reverse=True)[:10]

    prompt = make_prompt(enemy, recommendations)
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return {
        "enemy": {
            "id": enemy.id,
            "name": enemy.name,
            "range": enemy.range,
            "properties": [p.name for p in enemy.properties],
            "skills": [s.name for s in enemy.skills],
            "immunities": [i.name for i in enemy.immunities],
        },
        "recommendations": recommendations,
        "llm_response": response.text
    }




@router.post('/user-experience')
async def create_user_experience(
    experience_data: UserExperienceData, 
    crud: CRUD=Depends(get_crud)
):
    """사용자 경험 데이터를 저장합니다."""
    
    # 캐릭터 데이터를 JSON 형태로 변환
    characters_data = [
        {
            "character_id": char.character_id,
            "instincts": [
                {
                    "instinct_id": instinct.instinct_id,
                    "used": instinct.used
                }
                for instinct in char.instincts
            ]
        }
        for char in experience_data.characters
    ]
    
    # UserExperience 객체 생성
    user_experience = UserExperience(
        stage_id=experience_data.stage_id,
        characters_data="",  # 빈 문자열로 초기화
        result=experience_data.result,
        clear_time=experience_data.clear_time,
        difficulty_rating=experience_data.difficulty_rating
    )
    
    # JSON 문자열로 변환하여 저장
    user_experience.set_characters_data(characters_data)
    
    # 데이터베이스에 저장
    crud.create(user_experience)
    
    return Msg(msg="User experience data saved successfully")


@router.get('/user-experience/{stage_id}')
async def get_user_experiences_by_stage(
    stage_id: str,
    limit: int = 50,
    crud: CRUD=Depends(get_crud)
):
    """특정 스테이지의 사용자 경험 데이터를 조회합니다."""
    
    experiences = crud.read_all(
        UserExperience, 
        filters={'stage_id': stage_id},
        limit=limit
    )
    
    result = []
    for exp in experiences:
        characters_data = exp.get_characters_data()
        result.append({
            "id": exp.id,
            "stage_id": exp.stage_id,
            "characters": characters_data,
            "timestamp": exp.timestamp,
            "result": exp.result,
            "clear_time": exp.clear_time,
            "difficulty_rating": exp.difficulty_rating
        })
    
    return result


@router.get('/user-experience/stats/{stage_id}')
async def get_user_experience_stats(
    stage_id: str,
    crud: CRUD=Depends(get_crud)
):
    """특정 스테이지의 사용자 경험 통계를 조회합니다."""
    
    # 해당 스테이지의 모든 경험 데이터 조회
    experiences = crud.read_all(
        UserExperience, 
        filters={'stage_id': stage_id}
    )
    
    if not experiences:
        return {
            "stage_id": stage_id,
            "total_experiences": 0,
            "win_rate": 0,
            "most_used_characters": [],
            "instinct_usage_rate": 0,
            "avg_clear_time": 0,
            "avg_difficulty_rating": 0
        }
    
    # 통계 계산
    total_experiences = len(experiences)
    win_count = sum(1 for exp in experiences if exp.result == 'win')
    win_rate = (win_count / total_experiences * 100) if total_experiences > 0 else 0
    
    # 추가 통계 계산
    clear_times = [exp.clear_time for exp in experiences if exp.clear_time is not None]
    difficulty_ratings = [exp.difficulty_rating for exp in experiences if exp.difficulty_rating is not None]
    
    avg_clear_time = sum(clear_times) / len(clear_times) if clear_times else 0
    avg_difficulty_rating = sum(difficulty_ratings) / len(difficulty_ratings) if difficulty_ratings else 0
    
    # 캐릭터 사용 빈도 계산
    character_usage = {}
    instinct_usage_count = 0
    total_instinct_opportunities = 0
    
    for exp in experiences:
        characters_data = exp.get_characters_data()
        for char_data in characters_data:
            char_id = char_data['character_id']
            character_usage[char_id] = character_usage.get(char_id, 0) + 1
            
            # 각 본능별 사용 여부 계산
            instincts = char_data.get('instincts', [])
            for instinct_data in instincts:
                total_instinct_opportunities += 1
                if instinct_data.get('used', False):
                    instinct_usage_count += 1
    
    # 가장 많이 사용된 캐릭터 (상위 5개)
    most_used_characters = sorted(
        character_usage.items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:5]
    
    instinct_usage_rate = (instinct_usage_count / total_instinct_opportunities * 100) if total_instinct_opportunities > 0 else 0
    
    # 본능별 사용 통계 계산
    instinct_usage_stats = {}
    for exp in experiences:
        characters_data = exp.get_characters_data()
        for char_data in characters_data:
            instincts = char_data.get('instincts', [])
            for instinct_data in instincts:
                instinct_id = instinct_data['instinct_id']
                if instinct_id not in instinct_usage_stats:
                    instinct_usage_stats[instinct_id] = {"total": 0, "used": 0}
                instinct_usage_stats[instinct_id]["total"] += 1
                if instinct_data.get('used', False):
                    instinct_usage_stats[instinct_id]["used"] += 1
    
    # 본능별 사용률 계산
    instinct_usage_rates = [
        {
            "instinct_id": instinct_id,
            "usage_rate": round((stats["used"] / stats["total"] * 100), 2) if stats["total"] > 0 else 0,
            "total_opportunities": stats["total"],
            "used_count": stats["used"]
        }
        for instinct_id, stats in instinct_usage_stats.items()
    ]
    
    return {
        "stage_id": stage_id,
        "total_experiences": total_experiences,
        "win_rate": round(win_rate, 2),
        "most_used_characters": [
            {"character_id": char_id, "usage_count": count}
            for char_id, count in most_used_characters
        ],
        "instinct_usage_rate": round(instinct_usage_rate, 2),
        "instinct_usage_details": instinct_usage_rates,
        "avg_clear_time": round(avg_clear_time, 2),
        "avg_difficulty_rating": round(avg_difficulty_rating, 2)
    }
    

# @router.get("/stage/{stage_id}", dependencies=[Depends(set_request_data)])
# async def recommend_characters_by_stage(stage_id: str, top_k: int):

#     top5 = recommend_characters(stage_id=stage_id, top_k=top_k)
#     return top5



@router.get("/gemini/test")
async def test():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="Explain how AI works in a few words"
    )
    return response.text
