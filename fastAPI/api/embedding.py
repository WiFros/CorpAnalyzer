from fastapi import APIRouter, HTTPException
from schemas.embedding import EmbeddingResponse, EmbeddingBatchResponse
from models.embedding import dedup
from schemas.request import NewsItem, NewsBatchRequest
from typing import List
import pandas as pd

router = APIRouter()

@router.post("/", response_model=EmbeddingBatchResponse)
async def get_embeddings(request: List[NewsItem]):
    # Example data
    news_items = request
    # convert from json to pandas df
    df_pandas = pd.DataFrame([item.dict() for item in news_items])    
    deduf_df = dedup(df_pandas)
    
    res = []
    for _, row in deduf_df.iterrows():
        # Row 객체를 딕셔너리로 변환
        res.append(
            EmbeddingResponse(
                title=  row.title,
                description= row.description,
                pubDate = row.pubDate,
                link = row.link,
            )
)


    response = EmbeddingBatchResponse(
        status="success",
        message="Successfully deleted duplicates.",
        data= res
    )
    
    return response