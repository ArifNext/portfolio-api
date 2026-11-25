import smtplib
from email.message import EmailMessage
from typing import Optional
import traceback

from app.core.config import settings

def send_email(to_email: str, subject: str, body: str, reply_to: Optional[str] = None) -> None:
    message = EmailMessage()
    message["From"] = settings.mail_from
    message["To"] = to_email
    message["Subject"] = subject
    if reply_to:
        message["Reply-To"] = reply_to
    message.set_content(body)

    try:
        print(f"📧 ইমেইল পাঠানোর চেষ্টা করা হচ্ছে: {to_email} (Host: {settings.smtp_host}, Port: {settings.smtp_port})")
        with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(message)
        print("✅ ইমেইল সফলভাবে পাঠানো হয়েছে!")
    except Exception as error:
        print("❌ ইমেইল পাঠাতে ব্যর্থ হয়েছে!")
        print(f"Error Details: {error}")
        traceback.print_exc()