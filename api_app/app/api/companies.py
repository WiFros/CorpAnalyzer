from fastapi import APIRouter, HTTPException, Query
from app.models.company import CompanyList, Company
from app.database import collection

router = APIRouter()

@router.get("/companies/", response_model=CompanyList)
async def get_companies(page: int = Query(1, ge=1)):
    page_size = 10
    skip = (page - 1) * page_size

    total_companies = collection.count_documents({})

    companies = list(collection.find({}, {"corp_code": 1, "corp_name": 1, "_id": 0})
                     .skip(skip)
                     .limit(page_size))

    if not companies and page != 1:
        raise HTTPException(status_code=404, detail="Page not found")

    total_pages = -(-total_companies // page_size)  # Ceiling division

    return CompanyList(
        companies=[Company(**company) for company in companies],
        total=total_companies,
        page=page,
        total_pages=total_pages
    )