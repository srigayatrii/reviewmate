from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    GITHUB_WEBHOOK_SECRET: str
    GEMINI_API_KEY: str


    class Config:
        env_file = ".env"


settings = Settings()