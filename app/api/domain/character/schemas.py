from pydantic import BaseModel, Field
from typing import List, Optional
from ..skill.schemas import SkillInfo
from ..property.schemas import PropertyInfo



class CharacterInfo(BaseModel):
    id:     int
    name:   str
    atk1:   int
    atk2:   int
    atk3:   int
    hp:     int
    range:  int
    cost:   int
    kb:     int
    tba:    int
    speed:    int
    spawn:    int
    base_id:  int
    form:     int
    pre_atk1: int
    pre_atk2: int
    pre_atk3: int
    back_atk: int
    atk_type: int
    trait:    int
    long_distance1: int
    long_distance2: int
    immunity:   int
    atk_freq:   int
    ability_enabled: int

    skills: Optional[List[SkillInfo]] = []
    properties: Optional[List[PropertyInfo]] = []

    class Config:
        orm_mode = True
        from_attributes=True



class CharacterData(BaseModel):
    name:   str
    atk1:   int
    atk2:   int
    atk3:   int
    hp:     int
    range:  int
    cost:   int
    kb:     int
    tba:    int
    speed:    int
    spawn:    int
    base_id:  int
    form:     int
    pre_atk1: int
    pre_atk2: int
    pre_atk3: int
    back_atk: int
    atk_type: int
    trait:    int
    long_distance1: int
    long_distance2: int
    immunity:   int
    atk_freq:   int
    ability_enabled: int
    skills: Optional[List[int]] = []
    properties: Optional[List[int]] = []

    class Config:
        orm_mode = True
        from_attributes=True


class SearchInfo(BaseModel):
    skills: List[int] = []
    properties: List[int] = []


class CharacterList(BaseModel):
    data: List[CharacterInfo]
    total: int
    page: int
    page_size: int

    class Config:
        orm_mode = True
        from_attributes=True


