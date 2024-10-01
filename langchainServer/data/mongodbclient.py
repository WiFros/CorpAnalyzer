from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.news # == Mysql DB
collection = database.news # == Mysql Table

# 선택적으로 연결 종료를 위한 함수
async def close_db_connection():
    client.close()