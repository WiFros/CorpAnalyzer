from fastapi import APIRouter

router = APIRouter()

@router.post("/index")
async def index_document(i):
    return