from pydantic import BaseModel, Field
from typing import List, Optional
from ..skill.schemas import SkillInfo
from ..property.schemas import PropertyInfo



class EnemyInfo(BaseModel):
    id:     int
    name:   str
    atk1:   int
    atk2:   int
    atk3:   int
    hp:     int
    range:  int
    kb:     int
    money:  int
    speed:  int
    tba:    int
    pre_atk1: int
    pre_atk2: int
    pre_atk3: int
    back_atk: int
    atk_type: int
    trait:    int
    long_distance1: int
    long_distance2: int
    atk_freq:   int
    ability_enabled: int
    immunity:   int

    skills: Optional[List[SkillInfo]] = []
    properties: Optional[List[PropertyInfo]] = []

    class Config:
        orm_mode = True
        from_attributes=True


class EnemyData(BaseModel):
    name:   str
    atk1:   int
    atk2:   int
    atk3:   int
    hp:     int
    range:  int
    kb:     int
    money:  int
    speed:  int
    tba:    int
    pre_atk1: int
    pre_atk2: int
    pre_atk3: int
    back_atk: int
    atk_type: int
    trait:    int
    long_distance1: int
    long_distance2: int
    atk_freq:   int
    ability_enabled: int
    immunity:   int

    skills: Optional[List[int]] = []
    properties: Optional[List[int]] = []

    class Config:
        orm_mode = True
        from_attributes=True



class SearchInfo(BaseModel):
    skills: List[int] = []
    properties: List[int] = []