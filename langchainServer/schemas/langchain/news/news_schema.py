from pydantic import BaseModel,Field
from typing import Dict, List


class MoveDetail(BaseModel):
    field: str = Field(description="회사의 분야")
    current_activity: List[str] = Field(description="현재 하고 있는 일의 목록")

class CompanySummary(BaseModel):
    title: str = Field(description = "company의 뉴스 최신 동향")
    move : List[MoveDetail] = Field(description = "지금 하고 있는일 리스트")
    summary : str = Field(description= "move 내용을 기반으로 요약")