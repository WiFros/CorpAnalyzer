from pydantic import BaseModel, Field
from typing import List, Any, Dict


class Company(BaseModel):
    corp_code: str = Field(..., alias="company_id")
    corp_name: str = Field(..., alias="company_name")

    class Config:
        populate_by_name = True  # 원래 필드 이름으로도 값을 할당할 수 있도록 설정

class CompanyList(BaseModel):
    companies: List[Company]
    total: int
    page: int
    total_pages: int




class Move(BaseModel):
    field: str
    current_activity: List[str]

class Result(BaseModel):
    title: str
    move: List[Move]
    summary: str

class CompanyResult(BaseModel):
    _id: str
    result: Result
    company_name: str

class DartReportResponse(BaseModel):
    status: str
    data: Dict[str, Any]  # MongoDB 문서가 dictionary로 반환되므로 Dict로 타입 지정

    class Config:
        orm_mode = True  # MongoDB 데이터를 처리하기 위한 옵션