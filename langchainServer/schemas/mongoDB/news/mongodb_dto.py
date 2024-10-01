from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel

class NewsToMongo(BaseModel):
    company_name : str
    result : Dict
    created_at : datetime = datetime.utcnow()
    class Config:
        orm_mode = True  # MongoDB와 같이 ORM 구조를 지원하기 위해 설정
