from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str = Field(min_length=10)
    image: Optional[str] = None
    tech_stack: Optional[str] = None
    github_link: Optional[str] = None
    live_link: Optional[str] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=150)
    description: Optional[str] = Field(default=None, min_length=10)
    image: Optional[str] = None
    tech_stack: Optional[str] = None
    github_link: Optional[str] = None
    live_link: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    title: str
    description: str
    image: Optional[str]
    tech_stack: Optional[str]
    github_link: Optional[str]
    live_link: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)