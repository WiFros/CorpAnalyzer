from fastapi import FastAPI
from pydantic import BaseModel
from api import summarization, ner, embedding, news, dart
from api import preprocessing
import warnings
# warning 무시
warnings.filterwarnings('ignore')


app = FastAPI()


# API 라우터 등록
app.include_router(news.router, prefix="/news", tags=["news"])
app.include_router(dart.router, prefix="/dart", tags=["dart"])