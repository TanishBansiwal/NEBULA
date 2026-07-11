from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    GROQ_API_KEY: str
    GROQ_MODEL: str

    REDIS_URL: str

    APP_NAME: str
    APP_VERSION: str

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()