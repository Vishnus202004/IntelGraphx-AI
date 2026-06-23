from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str = "IntelGraphX AI"
    API_V1_STR: str = "/api/v1"


    DATABASE_URL: str = "sqlite+aiosqlite:///./intelgraphx.db"


    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440


    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str
    SMTP_PORT: int = 587
    SMTP_SERVER: str
    SMTP_STARTTLS: bool = True
    SMTP_SSL: bool = False
    SMTP_USE_CREDENTIALS: bool = True


    NEWS_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None


    LANGCHAIN_TRACING_V2: str = "false"
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: str = "intelgraphx-ai"


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
