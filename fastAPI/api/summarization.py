from fastapi import APIRouter, HTTPException
from schemas.summarization import SumBatchResponse, SumResponse
from models.summarization import summarization
from schemas.request import NewsItem, NewsBatchRequest

router = APIRouter()

@router.post("/", response_model=SumBatchResponse)
async def get_embeddings(request: NewsBatchRequest):
    # Example data
    news_items = request.items
    
    sum_data = summarization(news_items)
    
    response = SumBatchResponse(
        status="success",
        message="Successfully retrieved ner data.",
        data= sum_data
    )
    
    return response