# app/services/company_search.py

from motor.motor_asyncio import AsyncIOMotorDatabase
import math
import re

class CompanySearchService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def search_companies(self, query: str, search_type: str, page: int, size: int):
        skip = (page - 1) * size

        if search_type == "prefix":
            search_regex = f"^{re.escape(query)}"
        else:  # substring
            search_regex = f"{re.escape(query)}"

        search_condition = {"corp_name": {"$regex": search_regex, "$options": "i"}}

        # 총 결과 수 쿼리
        total = await self.db.companies.count_documents(search_condition)

        # 실제 결과 쿼리 (corp_name으로 정렬)
        cursor = self.db.companies.find(search_condition).sort("corp_name", 1).skip(skip).limit(size)
        companies = await cursor.to_list(length=size)

        total_pages = math.ceil(total / size)

        return {
            "companies": [
                {"company_id": str(company["_id"]), "company_name": company["corp_name"]}
                for company in companies
            ],
            "total": total,
            "page": page,
            "total_pages": total_pages
        }