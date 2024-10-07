from fastapi import APIRouter
from models.news import news_summarization
from typing import List
from langchain_core.output_parsers import PydanticOutputParser
from schemas.langchain.news.news_schema import CompanySummary
from data.elasticsearchclient import ESclient
from utils.news_util import company_summary_to_json
from crud.news.crud import create_result
import pandas as pd
import json

router = APIRouter()

@router.get("", response_model=CompanySummary)
async def summarize_news_move(company_name: str = ""):
    ESc = ESclient(path ="hi")
    index_name = "news_docs"
    print(company_name, index_name)
    # Fetch data from Elasticsearch
    search_query = {
    "query" :{
                "match" : {
            "company_names" : f"{company_name}"
        }
    },
    "size" : 50, # 최대 가져오는 뉴스 수
    "min_score" : 1.5, # 스코어 필터링
}
    result = ESc.adv_search(index_name, search_query)['hits']['hits']

    # send res(or rerank documents) to models
    news_result = news_summarization(company_name, result)
    
    # convert news_result in string with certain format to 
    parser = PydanticOutputParser(pydantic_object= CompanySummary)
    response = parser.parse(news_result)
    formatted_response = company_summary_to_json(response)
    return response