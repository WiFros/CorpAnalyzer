# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://admin:ssafya606@localhost:27017/admin"
    DB_NAME: str = "company_db"
    COLLECTION_NAME: str = "companies"

    class Config:
        env_file = ".env"

settings = Settings()
