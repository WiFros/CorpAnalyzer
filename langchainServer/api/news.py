from fastapi import APIRouter
from models.news import news_summarization
from typing import List
from langchain_core.output_parsers import PydanticOutputParser
from schemas.langchain.news.news_schema import CompanySummary
from data.elasticsearchclient import ESclient
from utils.news_util import company_summary_to_json
from crud.news.crud import create_result
from models.query_embedding import embedding_process
import pandas as pd
import json
import torch
from transformers import AutoModel, AutoTokenizer
import warnings
import dotenv
import os
warnings.filterwarnings(action='ignore')
router = APIRouter()
dotenv.load_dotenv()

@router.get("", response_model=CompanySummary)
async def summarize_news_move(company_name: str = ""):
    ESc = ESclient(path =os.getenv("ES_HOST"))
    index_name = os.getenv("ES_INDEX_NAME")
    size = 500
    output = embedding_process(company_name= company_name)
    body = {
    "size": size,
    "query": {
        "bool": {
        "must": [
            {
            "knn" : {
                "field": "embedding_vector",
                "query_vector":output,
                "k": 10000,
            }
            },
            {
            "match": {
                "company_names": f"{company_name}"
            }
            }
        ]
        }
    }
    }
    result = ESc.adv_search(index_name, body)['hits']['hits']

    # send res(or rerank documents) to models
    news_result = news_summarization(company_name, result)
    
    # convert news_result in string with certain format to 
    parser = PydanticOutputParser(pydantic_object= CompanySummary)
    response = parser.parse(news_result)
    formatted_response = company_summary_to_json(response)
    return response