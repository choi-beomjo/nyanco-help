from pydantic import BaseModel, Field
from typing import List, Optional
from ..skill.schemas import SkillInfo
from ..property.schemas import PropertyInfo



class EnemyInfo(BaseModel):
    id:     int
    name:   str
    atk:    int
    hp:     int
    range:  int
    kb:     int
    dps:    int
    money:  int
    speed:  int
    tba:    int
    target: str
    atk_sec:    int
    skills: Optional[List[SkillInfo]] = []
    properties: Optional[List[PropertyInfo]] = []

    class Config:
        orm_mode = True
        from_attributes=True


class EnemyData(BaseModel):
    name:   str
    atk:    int
    hp:     int
    range:  int
    kb:     int
    dps:    int
    money:  int
    speed:  int
    tba:    int
    target: str
    atk_sec:    int
    skills: Optional[List[int]] = []
    properties: Optional[List[int]] = []

    class Config:
        orm_mode = True
        from_attributes=True



class SearchInfo(BaseModel):
    skills: List[int] = []
    properties: List[int] = []