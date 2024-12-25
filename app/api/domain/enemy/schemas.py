from pydantic import BaseModel, Field
from typing import List, Optional
from ..skill.schemas import SkillInfo


class PropertyInfo(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True
        from_attributes=True


class EnemyInfo(BaseModel):
    id:     int
    atk:    int
    hp:     int
    range:  int
    skills: Optional[List[SkillInfo]] = []
    properties: Optional[List[PropertyInfo]] = []

    class Config:
        orm_mode = True
        from_attributes=True


class EnemyPost(BaseModel):
    atk:    int
    hp:     int
    range:  int
    skills: Optional[List[str]] = []
    properties: Optional[List[str]] = []

    class Config:
        orm_mode = True
        from_attributes=True