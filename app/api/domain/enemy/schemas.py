from pydantic import BaseModel, Field
from typing import List, Optional


class SkillInfo(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        from_attributes=True


class PropertyInfo(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True
        from_attributes=True


class EnemyInfo(BaseModel):
    atk:    int
    hp:     int
    range:  int
    skills: Optional[List[SkillInfo]] = []
    properties: Optional[List[PropertyInfo]] = []

    class Config:
        orm_mode = True
        from_attributes=True


