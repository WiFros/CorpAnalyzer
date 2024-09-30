from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://host.docker.internal:27017/"
    DB_NAME: str = "company_db"
    COLLECTION_NAME: str = "companies"

    class Config:
        env_file = ".env"

settings = Settings()
