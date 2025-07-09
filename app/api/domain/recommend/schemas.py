from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class InstinctUsageData(BaseModel):
    instinct_id: int
    used: bool = False  # 해당 본능 사용 여부


class CharacterUsageData(BaseModel):
    character_id: int
    instincts: List[InstinctUsageData]  # 각 본능별 사용 여부


class UserExperienceData(BaseModel):
    stage_id: int
    characters: List[CharacterUsageData]
    result: str  # 'win', 'lose', 'draw' - 필수 필드로 변경
    timestamp: Optional[datetime] = None
    # 추천 모델 학습을 위한 추가 데이터
    clear_time: Optional[int] = None  # 클리어 시간 (초)
    difficulty_rating: Optional[int] = None  # 사용자가 평가한 난이도 (1-5)


class UserExperienceResponse(BaseModel):
    id: int
    stage_id: int
    characters: List[CharacterUsageData]
    timestamp: datetime
    result: Optional[str] = None

    class Config:
        from_attributes = True 