from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services.routing import route_to_service
from app.utils.caching import cache, get_cache_key

router = APIRouter()


class RouteRequest(BaseModel):
    request_type: str
    data: dict


@router.post("/route_request")
async def route_request(request: RouteRequest):
    cache_key = get_cache_key(request.request_type, request.data)

    if cache_key in cache:
        return JSONResponse(content=cache[cache_key], headers={"X-Cache": "Hit"})

    result = await route_to_service(request.request_type, request.data)

    cache[cache_key] = result

    return JSONResponse(content=result, headers={"X-Cache": "Miss"})