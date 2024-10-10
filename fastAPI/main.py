from fastapi import FastAPI
from pydantic import BaseModel
from api import summarization, ner, embedding, dart_analyze
from api import preprocessing
import warnings
# warning 무시
warnings.filterwarnings('ignore')


app = FastAPI()


# API 라우터 등록
app.include_router(summarization.router, prefix="/summarize", tags=["summarization"])
app.include_router(ner.router, prefix="/ner", tags=["ner"])
app.include_router(embedding.router, prefix="/embedding", tags=["embedding"])
app.include_router(dart_analyze.router, prefix="/dart_analyze", tags=["dart_analyze"])
app.include_router(preprocessing.router, prefix="/preprocess", tags=["preprocess"])