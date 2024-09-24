from fastapi import APIRouter, HTTPException, Depends
from schemas.ner import NerResponse, NerBatchResponse
from schemas.preprocessing import PreprocessingResponse, PreprocessingBatchResponse
from models.ner import ner
from schemas.request import NewsItem
from schemas.summarization import SumBatchResponse, SumResponse
from models.summarization import summarization
from models.embedding import dedup
from typing import List
from data.elasticsearchclient import ESclient
from schemas.elasticsearch.request import NewsESSchema, BatchNewsESSchema
import pandas as pd

import json

router = APIRouter()


@router.post("/", response_model=NewsESSchema)
async def get_preprocess(request: List[NewsItem]):
    es_client = ESclient()
    # Example data
    news_items = request
    # convert from json to pandas df
    df_pandas = pd.DataFrame([item.dict() for item in news_items])
    
    dedup_df = dedup(df_pandas)
    # 1. ner
    ner_df = ner(dedup_df)
    # 2. summ
    summ_df = summarization(ner_df)
    
    #Dict로 변환.

    # 결과를 받아서 , pydantic 형식으로 반환
    res = []
    
    for _, row in summ_df.iterrows():
        # Row 객체를 딕셔너리로 변환
        res.append(
            NewsESSchema(
                title=  row.title,
                description= row.description,
                company_names =  row.company_names if row.company_names is not None else [],
                summary = row.summary,
                published_date = row.pubDate,
                link = row.link
            )
)
    res2 = [
    {
        "title": row.title,
        "description": row.description,
        "company_names": row.company_names if row.company_names is not None else [],
        "summary": row.summary
    }
    for _,row in summ_df.iterrows()
]

    es_client.index_docs("news_docs", res)
    response = BatchNewsESSchema(
        status="success",
        message="Successfully preprocessed data.",
        data= res
    )
    with open("./output.json",mode="w", encoding='utf-8') as f:
        f.write(json.dumps(res2, ensure_ascii=False, indent = 4))
    return response