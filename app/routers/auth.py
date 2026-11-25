from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.otp import EmailOnly, OtpVerify, PasswordReset
from app.schemas.user import UserCreate, UserLogin, UserOut, Token
from app.services import user_service, otp_service
from app.utility.mailer import send_email
from app.utility.security import create_access_token

router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if user_service.get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    return user_service.create_user(db, data)


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, data.email, data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Wrong email or password")

    return {"access_token": create_access_token(user.id), "token_type": "bearer"}


@router.post("/forgot-password")
def forgot_password(data: EmailOnly, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, data.email)

    if user is not None and otp_service.can_send_otp(db, data.email, otp_service.PURPOSE_RESET):
        code = otp_service.create_otp(db, data.email, otp_service.PURPOSE_RESET)
        body = otp_service.build_reset_mail(code)
        background_tasks.add_task(send_email, data.email, "Reset your password", body)

    # Same answer every time, so nobody can find out which emails are registered
    return {"message": "If the account exists, a reset code has been sent"}


@router.post("/verify-otp")
def verify_otp(data: OtpVerify, db: Session = Depends(get_db)):
    if not otp_service.verify_otp(db, data.email, data.code, otp_service.PURPOSE_RESET):
        raise HTTPException(status_code=400, detail="Wrong or expired code")

    return {"message": "Code verified, now set your new password"}


@router.post("/reset-password")
def reset_password(data: PasswordReset, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, data.email)
    if user is None or not otp_service.is_otp_verified(db, data.email, otp_service.PURPOSE_RESET):
        raise HTTPException(status_code=400, detail="Verify your code first")

    user_service.update_password(db, user, data.new_password)
    otp_service.delete_otp(db, data.email, otp_service.PURPOSE_RESET)
    return {"message": "Password changed, you can login now"}


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user