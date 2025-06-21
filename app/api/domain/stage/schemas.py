from pydantic import BaseModel, Field
from typing import List, Optional, Union
from ..enemy.schemas import EnemyInfo


class EnemyList(BaseModel):
    stage_id: str
    enemy_id: int
    spawn_count: Union[int, str]
    first_spawn: Union[int, str]
    respawn1: Union[int, str]
    respawn2: Union[int, str]
    health: Union[int, str]

    class Config:
        orm_mode = True
        from_attributes=True


class StageInfo(BaseModel):
    name: str
    stage_hp: int
    length: int
    max_enemies: int
    min_spawn: int
    difficulty: float
    enemies: List[EnemyList]

    class Config:
        orm_mode = True
        from_attributes=True


class StageList(BaseModel):
    data: List[StageInfo]
    total: int
    page: int
    page_size: int

    class Config:
        orm_mode = True
        from_attributes=True