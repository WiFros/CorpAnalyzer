from pydantic import BaseModel
from typing import List

class Company(BaseModel):
    corp_code: str
    corp_name: str

class CompanyList(BaseModel):
    companies: List[Company]
    total: int
    page: int
    total_pages: int