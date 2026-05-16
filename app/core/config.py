from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    telegram_bot_token: str
    webapp_url: str
    secret_key: str = "dev_secret"

    class Config:
        env_file = ".env"


settings = Settings()
