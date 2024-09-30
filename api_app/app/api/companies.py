from fastapi import APIRouter, HTTPException, Query
from app.models.company import CompanyList, Company
from app.database import collection

router = APIRouter()

@router.get("/companies/", response_model=CompanyList)
def get_companies(page: int = Query(1, ge=1)):
    page_size = 10
    skip = (page - 1) * page_size

    total_companies = collection.count_documents({})

    # MongoDB에서 corp_code와 corp_name을 가져오지만, 클라이언트에 반환할 때는 alias로 변환됨
    companies = list(collection.find({}, {"corp_code": 1, "corp_name": 1, "_id": 0})
                     .skip(skip)
                     .limit(page_size))

    if not companies and page != 1:
        raise HTTPException(status_code=404, detail="Page not found")

    total_pages = -(-total_companies // page_size)  # Ceiling division

    # Company 모델로 변환 시 Pydantic에서 자동으로 alias를 사용해 변환
    return CompanyList(
        companies=[Company.model_validate(company) for company in companies],
        total=total_companies,
        page=page,
        total_pages=total_pages
    )

