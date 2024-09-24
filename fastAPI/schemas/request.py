import datetime
from typing import List
from pydantic import BaseModel


# class NewsItem(BaseModel):
#     id: int
#     title: str
#     article: str
#     published_date: str  

class NewsItem(BaseModel):
    title : str
    description : str
    pubDate : str
    link : str

# class NewsItem(BaseModel):
#     title : str
#     description : str


class NewsBatchRequest(BaseModel):
    items: list[NewsItem]