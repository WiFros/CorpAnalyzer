from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NEWS_SERVICE_URL: str = "http://news_serv_app:8001"
    DART_SERVICE_URL: str = "http://dart_serv_app:8002"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()