# app/main.py

from fastapi import FastAPI
from app.api.companies import companies_router  # 여기를 수정했습니다
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Company Search API",
    description="An API for searching company information",
    version="0.1.0"
)
Instrumentator().instrument(app).expose(app)


# Include the router
app.include_router(companies_router, prefix="/api/companies", tags=["companies"])
# Optional: Add a root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Company Search API"}

# app/api/companies.py

from fastapi import APIRouter, Query, Depends
from app.services.company_search import CompanySearchService
from app.models.company import CompanyList
from app.database import get_database

companies_router = APIRouter()

@companies_router.get("/search", response_model=CompanyList)
async def search_companies(
    query: str = Query(..., min_length=1),
    search_type: str = Query("prefix", regex="^(prefix|substring)$"),
    page: int = Query(1, ge=1),
    db = Depends(get_database)
):
    company_search_service = CompanySearchService(db)
    await company_search_service.initialize_trie()
    results = await company_search_service.search_companies(query, search_type, page)
    return CompanyList(**results)