from fastapi import HTTPException
from app.config import settings

async def route_to_service(request_type: str):
    if request_type == "type1":
        url = f"{settings.FASTAPI2_URL}/process"
    elif request_type == "type2":
        url = f"{settings.FASTAPI3_URL}/process"
    else:
        raise HTTPException(status_code=400, detail="Invalid request type")