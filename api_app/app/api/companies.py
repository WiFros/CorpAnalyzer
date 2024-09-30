from fastapi import APIRouter, Query, Depends
from app.services.company_search import CompanySearchService
from app.models.company import CompanyList
from app.database import get_database

router = APIRouter()

@router.get("/search", response_model=CompanyList)
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