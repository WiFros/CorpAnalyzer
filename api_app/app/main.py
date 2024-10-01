# app/main.py

from fastapi import FastAPI
from app.api.companies import companies_router
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Company Search API",
    description="An API for searching company information",
    version="0.1.0"
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex="https?://localhost(:\d+)?",
)

# Prometheus 설정
Instrumentator().instrument(app).expose(app)

# 라우터 포함
app.include_router(companies_router, prefix="/api/companies", tags=["companies"])

# 루트 엔드포인트
@app.get("/")
async def root():
    return {"message": "Welcome to the Company Search API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)