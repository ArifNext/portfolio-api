from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SkillCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    level: int = Field(default=50, ge=0, le=100)
    icon: Optional[str] = None


class SkillOut(BaseModel):
    id: int
    name: str
    level: int
    icon: Optional[str]

    model_config = ConfigDict(from_attributes=True)