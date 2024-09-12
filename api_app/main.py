from fastapi import FastAPI
from app.api.v1 import endpoints  # API 엔드포인트 임포트

app = FastAPI()

# API 라우터 등록
app.include_router(endpoints.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to api_app"}
