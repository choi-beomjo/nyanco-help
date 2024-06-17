from pydantic import BaseModel, Field
from typing import List, Optional


class USER(BaseModel):
    id:     str
    name:   str
    email:  str


class UserInfo(BaseModel):
    name:   Optional[str]
    email:  Optional[str]
