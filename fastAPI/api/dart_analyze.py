from fastapi import APIRouter
from models.dart_analyze import process_rag
from fastapi import APIRouter, UploadFile, File
from schemas.dart_analyze import ReportUploadSchema
from fastapi import UploadFile

# FastAPI 라우터 설정
router = APIRouter()

@router.post("/")
async def dart_analyze(file: UploadFile, company_name: str):
    # RAG 처리 호출
    report = await process_rag(file, company_name)
    return report

