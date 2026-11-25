from pydantic import BaseModel, EmailStr, Field, field_validator


class EmailOnly(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, value: str) -> str:
        return value.lower()


class OtpVerify(BaseModel):
    email: EmailStr
    code: str = Field(pattern=r"^\d{6}$")

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, value: str) -> str:
        return value.lower()


class PasswordReset(BaseModel):
    email: EmailStr
    new_password: str = Field(min_length=8, max_length=64)

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, value: str) -> str:
        return value.lower()

    @field_validator("new_password")
    @classmethod
    def check_password(cls, value: str) -> str:
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must have at least one letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must have at least one number")
        return value