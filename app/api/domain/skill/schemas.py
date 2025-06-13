from pydantic import BaseModel, Field
from typing import List, Optional


class SkillInfo(BaseModel):
    id: int
    name: str
    category: str

    class Config:
        orm_mode = True
        from_attributes=True


class SkillPost(BaseModel):
    name: str
    category: str

    class Config:
        orm_mode = True
        from_attributes=True