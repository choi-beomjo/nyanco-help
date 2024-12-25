from pydantic import BaseModel, Field
from typing import List, Optional


class SkillInfo(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        from_attributes=True