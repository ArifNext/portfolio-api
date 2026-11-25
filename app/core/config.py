from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    token_expire_minutes: int = 60
    frontend_url: str = "http://localhost:3000"

    smtp_host: str
    smtp_port: int = 465
    smtp_user: str
    smtp_password: str
    mail_from: str
    admin_email: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()