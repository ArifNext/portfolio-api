from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class MessageCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class MessageOut(BaseModel):
    id: int
    name: str
    email: str
    message: str
    created_at: datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True