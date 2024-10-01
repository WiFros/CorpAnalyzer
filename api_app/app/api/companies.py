# app/api/companies.py

from fastapi import APIRouter, Query, Depends, HTTPException
from app.services.company_search import CompanySearchService
from app.services.hotKeyword_search import hotKeywordService
from app.models.company import CompanyList
from app.models.hotkeyword import KeywordList
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
    try:
        results = await company_search_service.search_companies(query, search_type, page)
        return CompanyList(**results)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@companies_router.get("/hotkeyword", response_model=KeywordList)
async def company_hotkeyword(
    corp_name: str ,
):
    hotkeyword_service = hotKeywordService(corp_name)
    try:
        results = await hotkeyword_service.fetch_hotkeyword()
        return KeywordList(**results)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))