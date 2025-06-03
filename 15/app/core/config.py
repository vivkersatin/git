from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "REST API 學習平台"
    debug_mode: bool = True
    database_url: str = "sqlite:///./learning.db"

    class Config:
        env_file = ".env"

settings = Settings()