from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.mongo import get_collection


class NewsSummaryService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def summary_news(self, company_name: str):

        company_cursor = self.db.news_report.find({"company_name": company_name})

        # 데이터를 리스트로 변환하여 결과 받기
        companies = await company_cursor.to_list(length=100)  # 최대 100개의 결과 가져오기

        if companies:
            return companies
        return None