from pydantic import BaseModel, Field
from typing import List, Optional


class EnemyInfo(BaseModel):
    atk:    int
    hp:     int
    range:  int
    skills: Optional[List[str]] = []
    properties: Optional[List[str]] = []