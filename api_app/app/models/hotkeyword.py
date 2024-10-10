from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

class KeywordList(BaseModel):
    corp_name: str
    keywords: List[str] # hot keyword

class KeywordNews(BaseModel):
    title: str
    pubDate: str
    link: str

class KeywordListWithNews(BaseModel):
    corp_name: str
    keywords: Dict[str,List[KeywordNews]] # hot keyword

