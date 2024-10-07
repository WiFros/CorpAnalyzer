import datetime
from typing import List
from pydantic import BaseModel

class NewsESSchema(BaseModel):
    title: str
    description : str
    company_names : List[str]
    summary : str
    published_date: str
    link : str
    # published_date: datetime 

class BatchNewsESSchema(BaseModel):
    data : List[NewsESSchema]

