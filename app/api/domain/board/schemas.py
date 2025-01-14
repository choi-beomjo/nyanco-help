from pydantic import BaseModel, Field
from typing import List, Optional


class SearchInfo(BaseModel):
    title: str


class Post(BaseModel):
    title:      str
    contents:   str

    class Config:
        orm_mode = True
        from_attributes=True


class PostInfo(BaseModel):
    id:         int
    title:      str
    contents:   str

    class Config:
        orm_mode = True
        from_attributes=True