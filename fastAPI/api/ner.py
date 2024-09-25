from fastapi import APIRouter, HTTPException
from schemas.ner import NerResponse, NerBatchResponse
from models.ner import ner
from schemas.request import NewsItem, NewsBatchRequest
from pyspark.sql import SparkSession
from typing import List

import pandas as pd

router = APIRouter()

@router.post("/", response_model=NerBatchResponse)
async def ner_function(request: List[NewsItem]):
    # Example data
    news_items = request
    df_pandas = pd.DataFrame([item.dict() for item in news_items])
    ner_data = ner(df_pandas)
    
    res = []
    for _, row in ner_data.iterrows():
        # Row 객체를 딕셔너리로 변환
        res.append(
            NerResponse(
                title=  row.title,
                description= row.description,
                company_names =  row.company_names if row.company_names is not None else [],
                pubDate = row.pubDate,
                link = row.link
            )
)

    response = NerBatchResponse(
        status="success",
        message="Successfully extracted ner data.",
        data= res
    )
    
    return response