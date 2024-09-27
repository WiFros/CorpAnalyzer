from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from app.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the API Gateway"}

@app.api_route("/news/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def news_route(request: Request, path: str):
    client = httpx.AsyncClient(base_url=settings.NEWS_SERVICE_URL)
    try:
        response = await client.request(
            method=request.method,
            url=f"/{path}",
            headers={key: value for (key, value) in request.headers.items() if key != "host"},
            data=await request.body(),
        )
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except httpx.HTTPStatusError as exc:
        return JSONResponse(
            content={"detail": str(exc)},
            status_code=exc.response.status_code
        )
    finally:
        await client.aclose()

@app.api_route("/dart/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def dart_route(request: Request, path: str):
    client = httpx.AsyncClient(base_url=settings.DART_SERVICE_URL)
    try:
        response = await client.request(
            method=request.method,
            url=f"/{path}",
            headers={key: value for (key, value) in request.headers.items() if key != "host"},
            data=await request.body(),
        )
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except httpx.HTTPStatusError as exc:
        return JSONResponse(
            content={"detail": str(exc)},
            status_code=exc.response.status_code
        )
    finally:
        await client.aclose()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)