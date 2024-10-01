from pydantic import BaseModel, Field
from typing import List


class KeywordList(BaseModel):
    corp_name: str
    keywords: List[str] # hot keyword

