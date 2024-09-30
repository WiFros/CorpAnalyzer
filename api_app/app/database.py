from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.DB_NAME]
collection = database[settings.COLLECTION_NAME]

async def get_database():
    return database

async def get_collection():
    return collection