from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.message import MessageCreate

def create_message(db: Session, user_id: Optional[int], data: MessageCreate) -> Message:
    db_message = Message(
        name=data.name,
        email=data.email,
        message=data.message,
        user_id=user_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_all_messages(db: Session) -> List[Message]:
    return db.query(Message).order_by(Message.created_at.desc()).all()