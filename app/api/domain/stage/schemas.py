from pydantic import BaseModel, Field
from typing import List, Optional


class StageInfo(BaseModel):
    name: str