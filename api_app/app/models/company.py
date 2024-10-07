from pydantic import BaseModel, Field
from typing import List

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


class News(BaseModel):
    title:str
    link:str



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
    news: List[News]
