from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.dependencies import require_admin
from app.schemas.message import MessageCreate, MessageOut
from app.services import message_service
from app.utility.mailer import send_email

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("", response_model=MessageOut, status_code=201)
def send_message(
        data: MessageCreate,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
):
    # ডাটাবেসে সেভ করা (user_id=None পাঠানো হচ্ছে কারণ ইউজার লগইন করেনি)
    # আপনার message_service.py-তে create_message ফাংশনটি যেন user_id=None সাপোর্ট করে, সেটি নিশ্চিত করবেন।
    saved = message_service.create_message(db, user_id=None, data=data)

    # ইমেইলের বডি তৈরি
    body = (
        f"Name: {data.name}\n"
        f"Email: {data.email}\n\n"
        f"Message:\n{data.message}"
    )

    # ব্যাকগ্রাউন্ড টাস্কে ইমেইল পাঠানো
    background_tasks.add_task(
        send_email,
        settings.admin_email,
        "New message from your portfolio",
        body,
        data.email,  # reply_to হিসেবে ক্লায়েন্টের ইমেইল
    )

    return saved


@router.get("", response_model=List[MessageOut], dependencies=[Depends(require_admin)])
def list_messages(db: Session = Depends(get_db)):
    return message_service.get_all_messages(db)