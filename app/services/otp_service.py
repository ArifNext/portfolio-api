import secrets
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.email_otp import EmailOtp
from app.utility.security import hash_password, verify_password

PURPOSE_RESET = "reset_password"

OTP_EXPIRE_MINUTES = 10
MAX_ATTEMPTS = 5
RESEND_WAIT_SECONDS = 60


def get_otp(db: Session, email: str, purpose: str):
    return (
        db.query(EmailOtp)
        .filter(EmailOtp.email == email, EmailOtp.purpose == purpose)
        .first()
    )


def can_send_otp(db: Session, email: str, purpose: str) -> bool:
    """False if an OTP was sent to this email less than 60 seconds ago."""
    otp = get_otp(db, email, purpose)
    if otp is None:
        return True
    wait_until = otp.created_at + timedelta(seconds=RESEND_WAIT_SECONDS)
    return datetime.utcnow() >= wait_until


def create_otp(db: Session, email: str, purpose: str) -> str:
    """Saves a new OTP (hashed) and returns the plain code to email."""
    delete_otp(db, email, purpose)

    code = f"{secrets.randbelow(1000000):06d}"
    otp = EmailOtp(
        email=email,
        purpose=purpose,
        code_hash=hash_password(code),
        expires_at=datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES),
    )
    db.add(otp)
    db.commit()
    return code


def verify_otp(db: Session, email: str, code: str, purpose: str) -> bool:
    """Checks the code. If it is right, the OTP stays saved as verified."""
    otp = get_otp(db, email, purpose)
    if otp is None:
        return False

    if otp.expires_at < datetime.utcnow() or otp.attempts >= MAX_ATTEMPTS:
        db.delete(otp)
        db.commit()
        return False

    if not verify_password(code, otp.code_hash):
        otp.attempts += 1
        db.commit()
        return False

    otp.is_verified = True
    otp.expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)
    db.commit()
    return True


def is_otp_verified(db: Session, email: str, purpose: str) -> bool:
    otp = get_otp(db, email, purpose)
    if otp is None or not otp.is_verified:
        return False

    if otp.expires_at < datetime.utcnow():
        db.delete(otp)
        db.commit()
        return False

    return True


def delete_otp(db: Session, email: str, purpose: str) -> None:
    db.query(EmailOtp).filter(
        EmailOtp.email == email, EmailOtp.purpose == purpose
    ).delete()
    db.commit()


def build_reset_mail(code: str) -> str:
    return (
        f"Your password reset code is: {code}\n\n"
        f"This code expires in {OTP_EXPIRE_MINUTES} minutes.\n"
        "If you did not ask for a password reset, ignore this email."
    )