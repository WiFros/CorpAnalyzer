from fastapi import APIRouter, HTTPException
from schemas.embedding import EmbeddingResponse, EmbeddingBatchResponse
from models.embedding import dedup
from schemas.request import NewsItem, NewsBatchRequest

router = APIRouter()

@router.post("/", response_model=EmbeddingBatchResponse)
async def get_embeddings(request: NewsBatchRequest):
    # Example data
    news_items = request.items
    
    embeddings_data = dedup(news_items)
    
    response = EmbeddingBatchResponse(
        status="success",
        message="Successfully retrieved embeddings.",
        data= embeddings_data
    )
    
    return response