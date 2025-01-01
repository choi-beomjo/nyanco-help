from pydantic import BaseModel, Field
from typing import List, Optional
from ..skill.schemas import SkillInfo
from ..property.schemas import PropertyInfo



class CharacterInfo(BaseModel):
    id:     int
    name:   str
    atk:    int
    hp:     int
    range:  int
    grade:  str
    skills: Optional[List[SkillInfo]] = []
    properties: Optional[List[PropertyInfo]] = []

    class Config:
        orm_mode = True
        from_attributes=True



class CharacterData(BaseModel):
    name:   str
    atk:    int
    hp:     int
    range:  int
    grade:  str
    skills: Optional[List[int]] = []
    properties: Optional[List[int]] = []

    class Config:
        orm_mode = True
        from_attributes=True


class SearchInfo(BaseModel):
    skills: List[int] = []
    properties: List[int] = []