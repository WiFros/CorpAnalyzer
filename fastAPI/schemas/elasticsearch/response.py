import datetime
from typing import List
from pydantic import BaseModel

class NewsESSchema(BaseModel):
    id : int
    title: str
    article : str
    company_names : List[str]
    # published_date: datetime 

class NerBatchResponse(BaseModel):
    # 여러개가 왔을때 묶어서 보내기.
    status: str
    message: str
    data: List[NerResponse]