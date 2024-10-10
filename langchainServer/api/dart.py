from fastapi import APIRouter, HTTPException
from schemas.request import NewsItem, NewsBatchRequest
from typing import List
import pandas as pd

router = APIRouter()

@router.post("", response_model=List[NewsItem])
async def get_embeddings(request: List[NewsItem]):
#     # Example data
#     news_items = request
#     # convert from json to pandas df
#     df_pandas = pd.DataFrame([item.dict() for item in news_items])    
#     # deduf_df = dedup(df_pandas)
#     ded
#     res = []
#     for _, row in deduf_df.iterrows():
#         # Row 객체를 딕셔너리로 변환
#         res.append(
#             NewsItem(
#                 title=  row.title,
#                 description= row.description,
#                 pubDate = row.pubDate,
#                 link = row.link,
#             )
# )


#     response = NewsBatchRequest(
#         status="success",
#         message="Successfully deleted duplicates.",
#         data= res
#     )
    raise NotImplementedError("이 기능은 아직 구현되지 않았습니다.")
    