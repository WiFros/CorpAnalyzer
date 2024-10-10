from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.DB_NAME]
collection = database[settings.COLLECTION_NAME]
dart_collection= database[settings.DART_COLLECTION_NAME]

async def get_database():
    return database

async def get_collection():
    return collection

async def get_dart_collection():
    return dart_collection

async def test_connection():
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Connection failed: {e}")