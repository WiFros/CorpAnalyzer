from fastapi import APIRouter, HTTPException
from schemas.summarization import SumBatchResponse, SumResponse
from models.summarization import summarization
from schemas.request import NewsItem, NewsBatchRequest
from schemas.ner import NerResponse
from typing import List
from data.elasticsearchclient import ESclient

import pandas as pd
router = APIRouter()

@router.post("", response_model=SumBatchResponse)
async def summ_function(request: List[NerResponse]):
    # Example data
    news_items = request
    
    df_pandas = pd.DataFrame([item.dict() for item in news_items])
    sum_data = summarization(df_pandas)
    
    res = []
    for _, row in sum_data.iterrows():
        # Row 객체를 딕셔너리로 변환
        res.append(
            SumResponse(
                title=  row.title,
                description= row.description,
                company_names =  row.company_names if row.company_names is not None else [],
                pubDate = row.pubDate,
                link = row.link,
                summary = row.summary
            )
)

    # es_client = ESclient()
    # es_client.index_docs("news_docs", res)
    response = SumBatchResponse(
        status="success",
        message="Successfully extracted summary data.",
        data= res
    )
    
    return response