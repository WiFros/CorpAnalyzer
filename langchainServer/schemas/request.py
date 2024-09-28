import datetime
from typing import List
from pydantic import BaseModel


class NewsItem(BaseModel):
    title : str
    description : str
    pubDate : str
    link : str

class NewsBatchRequest(BaseModel):
    items: list[NewsItem]