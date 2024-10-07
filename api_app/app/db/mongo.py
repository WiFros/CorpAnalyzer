from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

async def connect_to_mongo():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    try:
        # 연결 테스트
        await client.admin.command('ismaster')
        print("Successfully connected to MongoDB")
        return client
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        return None

async def get_database():
    client = await connect_to_mongo()
    if client:
        return client[settings.DB_NAME]
    return None
async def close_mongo_connection():
    client = await get_database()
    if client:
        client.close()
async def get_collection():
    db = await get_database()
    if db:
        return db[settings.COLLECTION_NAME]
    return None