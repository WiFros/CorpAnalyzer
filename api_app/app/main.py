from fastapi import FastAPI
from app.services.company_search import CompanySearchService

app = FastAPI()
company_search_service = None

@app.on_event("startup")
async def startup_event():
    global company_search_service
    company_search_service = CompanySearchService()
    await company_search_service.initialize_trie()

from app.api import companies
app.include_router(companies.router, prefix="/api/companies", tags=["companies"])