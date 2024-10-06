from pydantic import BaseModel
from fastapi import UploadFile, File
from typing import List, Dict
from typing import Optional

# 요청 데이터 모델 정의
class AnalyzeRequest(BaseModel):
    company_name: str
    
from pydantic import BaseModel
from fastapi import UploadFile, File
from typing import Optional

# 파일 업로드 요청 스키마
class ReportUploadSchema(BaseModel):
    file: UploadFile = File(...)
    company_name: str

# HTML 파일 업로드 요청 스키마
class FileUploadSchema(BaseModel):
    file: UploadFile = File(..., description="파일 업로드")
    company_name: str

class ReportSchema(BaseModel):
    report_data: dict

