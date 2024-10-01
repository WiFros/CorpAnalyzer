import datetime
from typing import List
from pydantic import BaseModel

class SumResponse(BaseModel):
    title : str
    description : str
    pubDate : str
    link : str
    company_names : List[str]
    summary : str
    # published_date: datetime 

class SumBatchResponse(BaseModel):
    # 여러개가 왔을때 묶어서 보내기.
    status: str
    message: str
    data: List[SumResponse]