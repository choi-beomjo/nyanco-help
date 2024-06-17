from pydantic import BaseModel, Field
from typing import List, Optional


class User(BaseModel):
    id:     str
    name:   str
    email:  str

    class Config:
        orm_mode = True


class UserInfo(BaseModel):
    name:   Optional[str]
    email:  Optional[str]
