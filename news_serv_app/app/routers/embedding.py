from fastapi import APIRouter

router = APIRouter()

@router.post("/embed")
async def embed_text():
    return