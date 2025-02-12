from pydantic import BaseModel, Field
from typing import List, Optional
from ..enemy.schemas import EnemyInfo


class StageInfo(BaseModel):
    name: str
    enemies: Optional[List[EnemyInfo]] = []

    class Config:
        orm_mode = True
        from_attributes=True
