from fastapi import APIRouter
from models.dart_analyze import process_rag, measure_process_time, clean_text
from fastapi import APIRouter, UploadFile, File
from schemas.dart_analyze import ReportUploadSchema
from fastapi import UploadFile
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from bson import ObjectId
import torch
# FastAPI 라우터 설정
router = APIRouter()

from gridfs import GridFSBucket
import base64
import time


client = AsyncIOMotorClient("mongodb://admin:ssafya606@j11a606.p.ssafy.io:27017/admin?authSource=admin")
db = client['company_db']
fs = AsyncIOMotorGridFSBucket(db)

# @router.post("/mongo/")
async def get_files_by_corp_name(corp_name: str):
    cursor = db['fs.files'].find({"metadata.corp_name": corp_name})

    text_content = ""  # 모든 텍스트 데이터를 저장할 변수

    async for file_doc in cursor:
        grid_out = await fs.open_download_stream(file_doc['_id'])
        file_data = await grid_out.read()

        try:
            # base64 디코딩 후 utf-8 텍스트로 변환
            decoded_data = file_data.decode('utf-8')
            # 텍스트 데이터를 변수에 저장
            text_content += decoded_data + "\n\n"  # 각 파일 데이터를 구분하기 위해 개행 추가
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    return text_content

@router.post("/")
async def dart_analyze(company_name: str):

    start_time1 = time.time()  # 요청 처리 시작 시간

    # MongoDB에서 기업 데이터 갖고 오기
    start_time = time.time()
    dart_data = get_files_by_corp_name(company_name)

    start_time = measure_process_time(start_time, "Mongo")

    # RAG 처리 호출
    report = await process_rag(dart_data, company_name)

    end_time = time.time()  # 요청 처리 완료 시간
    elapsed_time = end_time - start_time1  # 경과 시간 계산

    print(f"총 처리 시간: {elapsed_time:.2f}초")  # 소수점 두 자리까지 출력

    return report

# Test3 - text_content 변수에 저장
@router.post("/mongoTest/")
async def get_files_by_corp_name1(corp_name: str):
    cursor = db['fs.files'].find({"metadata.corp_name": corp_name})

    text_content = ""  # 모든 텍스트 데이터를 저장할 변수
    
    async for file_doc in cursor:
        grid_out = await fs.open_download_stream(file_doc['_id'])
        file_data = await grid_out.read()

        try:
            # base64 디코딩 후 utf-8 텍스트로 변환
            decoded_data = file_data.decode('utf-8')
            # 텍스트 데이터를 변수에 저장
            text_content += decoded_data + "\n\n"  # 각 파일 데이터를 구분하기 위해 개행 추가
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    cleaned_text = clean_text(text_content)
    return {"status": "success", "message": cleaned_text}

# # Test 2 - txt 파일로 저장
# @router.post("/mongo/")
# async def get_files_by_corp_name(corp_name: str):
#     cursor = db['fs.files'].find({"metadata.corp_name": corp_name})

#     async with aiofiles.open("output.txt", mode="w", encoding="utf-8") as file:  # "a":텍스트 파일 append 모드로 열기(추가), "w": write 모드로 열기(덮어쓰기)
#         async for file_doc in cursor:
#             grid_out = await fs.open_download_stream(file_doc['_id'])
#             file_data = await grid_out.read()

#             try:
#                 # base64 디코딩 후 utf-8 텍스트로 변환
#                 decoded_data = file_data.decode('utf-8')
#                 await file.write(decoded_data + "\n\n")
#             except Exception as e:
#                 return {"status": "error", "message": str(e)}
            
#     return {"status": "success", "message": "content"}

# # Test 1 - 성공
# @router.post("/mongo/")
# async def get_files_by_corp_name(corp_name: str):
#     cursor = db['fs.files'].find({"metadata.corp_name": corp_name})
    
#     async with aiofiles.open("output.txt", mode="w", encoding="utf-8") as file:  # 텍스트 파일을 append 모드로 열기
#         async for file_doc in cursor:
#             grid_out = await fs.open_download_stream(file_doc['_id'])
#             file_data = await grid_out.read()

#             try:
#                 # base64 디코딩 후 utf-8 텍스트로 변환
#                 decoded_data = file_data.decode('utf-8')
#                 await file.write(f"Filename: {file_doc['filename']}\n")
#                 await file.write(decoded_data + "\n\n")
#             except Exception as e:
#                 return {"status": "error", "message": str(e)}

#     return {"status": "success", "message": "Data saved to output.txt", "data": file}



# async def get_files_by_corp_name(corp_name: str):
#     # fs.files 컬렉션에서 corp_name으로 여러 문서 조회
#     cursor = db['fs.files'].find({"metadata.corp_name": corp_name})
#     files = []
    
#     async for file_doc in cursor:
#         grid_out = await fs.open_download_stream(file_doc['_id'])
#         file_data = await grid_out.read()

#         try:
#             # base64 디코딩 후 utf-8로 텍스트 변환
#             decoded_data = base64.b64decode(file_data)
#             files.append({"filename": file_doc["filename"], "content": decoded_data})
#         except Exception as e:
#             return {"status": "error", "message": str(e)}

#     return {"status": "success", "files": files} if files else {"status": "error", "message": "No documents found"}



