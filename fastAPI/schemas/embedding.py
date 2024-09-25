import datetime
from typing import List
from pydantic import BaseModel

class EmbeddingResponse(BaseModel):
    title : str
    description : str
    pubDate : str
    link : str
    # published_date: datetime 

class EmbeddingBatchResponse(BaseModel):
    # 여러개가 왔을때 묶어서 보내기.
    status: str
    message: str
    data: List[EmbeddingResponse]
    
    