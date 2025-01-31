from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_URL: str = "http://localhost:8000"
    NGROK_TOKEN: str
    META_WEBHOOK_TOKEN: str
    META_ACCESS_TOKEN: str
    META_ID_NUMBER: str

    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()
