from fastapi import APIRouter, HTTPException
from schemas.ner import NerResponse, NerBatchResponse
from models.ner import ner
from schemas.request import NewsItem, NewsBatchRequest
from pyspark.sql import SparkSession

router = APIRouter()

@router.post("/", response_model=NerBatchResponse)
async def get_embeddings(request: NewsBatchRequest):
    # Example data
    news_items = request.items
    
    ner_data = ner(news_items)
    
    response = NerBatchResponse(
        status="success",
        message="Successfully retrieved ner data.",
        data= ner_data
    )
    
    return response