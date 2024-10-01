# app/services/company_search.py

from app.utils.optimized_search import OptimizedSearch
from app.models.company import Company
from motor.motor_asyncio import AsyncIOMotorDatabase
from cachetools import TTLCache
import asyncio

class CompanySearchService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.search_engine = OptimizedSearch()
        self.cache = TTLCache(maxsize=1000, ttl=3600)  # Cache for 1 hour
        self.initialization_lock = asyncio.Lock()
        self.is_initialized = False

    async def initialize_search_engine(self):
        async with self.initialization_lock:
            if not self.is_initialized:
                async for company in self.db.companies.find({}, {"corp_code": 1, "corp_name": 1, "_id": 0}):
                    self.search_engine.add_company(company)
                self.is_initialized = True

    async def search_companies(self, query: str, search_type: str = 'prefix', page: int = 1, page_size: int = 10):
        await self.initialize_search_engine()

        cache_key = f"{query}:{search_type}:{page}:{page_size}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        if search_type == 'prefix':
            results = self.search_engine.search_prefix(query)
        elif search_type == 'substring':
            results = self.search_engine.search_substring(query)
        else:
            raise ValueError("Invalid search type. Use 'prefix' or 'substring'.")

        total = len(results)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_results = results[start:end]

        companies = [Company.model_validate(company) for company in paginated_results]
        total_pages = -(-total // page_size)  # Ceiling division

        response = {
            "companies": companies,
            "total": total,
            "page": page,
            "total_pages": total_pages
        }

        self.cache[cache_key] = response
        return response