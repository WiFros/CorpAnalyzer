import datetime
from typing import List
from pydantic import BaseModel

class NerResponse(BaseModel):
    title : str
    description : str
    pubDate : str
    link : str
    company_names : List[str]
    embedding_vector : List[float]
    # published_date: datetime 

class NerBatchResponse(BaseModel):
    # 여러개가 왔을때 묶어서 보내기.
    status: str
    message: str
    data: List[NerResponse]