from fastapi import APIRouter, Query
from app.main import company_search_service
from app.models.company import CompanyList

router = APIRouter()

@router.get("/search", response_model=CompanyList)
async def search_companies(
    query: str = Query(..., min_length=1),
    search_type: str = Query("prefix", regex="^(prefix|substring)$"),
    page: int = Query(1, ge=1)
):
    results = company_search_service.search_companies(query, search_type, page)
    return CompanyList(**results)