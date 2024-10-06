from models.dart_analyze import process_rag, measure_process_time, clean_text
from fastapi import APIRouter, HTTPException
from schemas.dart_analyze import ReportUploadSchema
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
import torch
# FastAPI 라우터 설정
router = APIRouter()

from gridfs import GridFSBucket
import base64
import time
from datetime import datetime

async def startup_event():
    # 'company_name' 필드에 고유 인덱스 설정
    await dart_collection.create_index([("company_name", 1)], unique=True)

# MongoDB 클라이언트 설정
client = AsyncIOMotorClient("mongodb://admin:ssafya606@j11a606.p.ssafy.io:27017/admin?authSource=admin")
db = client['company_db']
fs = AsyncIOMotorGridFSBucket(db)

# 결과를 저장할 컬렉션 지정
dart_collection = db['dart_reports']


# 회사 이름이 저장된 파일을 읽어오기
def load_company_names(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        company_names = file.read().splitlines()
    return company_names

@router.post("/multi/")
async def process_multiple_companies(): # 반복 호출을 위한 함수
    company_names = load_company_names("data\data.txt")  # data.txt에서 회사 이름 로드
    results = []

    for company_name in company_names[10:100]:  # 최대 N개의 회사 이름만 처리
        try:
            # dart_analyze 메서드 호출
            result = await dart_analyze(company_name)
            results.append(result)  # 결과를 리스트에 저장
        except Exception as e:
            print(f"{company_name} 처리 중 오류 발생: {str(e)}")
    
    return results


@router.post("/mongo/")
async def get_files_by_corp_name(corp_name: str):
    cursor = db['fs.files'].find({"metadata.corp_name": corp_name})

    text_content = ""  # 모든 텍스트 데이터를 저장할 변수
    file_found = False  # 기업 파일 존재 여부 확인용 변수
    async for file_doc in cursor:
        file_found = True  # 파일이 존재하면 True로 변경
        try:
            grid_out = await fs.open_download_stream(file_doc['_id'])
            file_data = await grid_out.read()
            # base64 디코딩 후 utf-8 텍스트로 변환
            decoded_data = file_data.decode('utf-8')
            # 텍스트 데이터를 변수에 저장
            text_content += decoded_data + " " # 띄어쓰기 추가
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    # 기업 파일이 없을 경우 예외 처리        
    if not file_found:
        raise HTTPException(status_code=404, detail=f"'{corp_name}'에 해당하는 데이터를 찾을 수 없습니다.")

    return text_content



@router.post("/")
async def dart_analyze(company_name: str):

    start_time1 = time.time()  # 요청 처리 시작 시간

    dart_data = get_files_by_corp_name(company_name)

    # RAG 처리 호출
    report = await process_rag(dart_data, company_name)

    dart_report = {
        "company_name": company_name,  # 상위 레벨에 회사명 포함
        "result": report,  # 분석 결과
        "created_at": datetime.now()  # 저장 시각
    }

    startup_event()

    try:
        # MongoDB에 데이터 덮어쓰기
        result = await dart_collection.replace_one(
            {"company_name": company_name},  # 필터: company_name으로 기존 문서 찾기
            dart_report,  # 덮어쓸 새로운 데이터
            upsert=True  # 문서가 없으면 새로 삽입
        )

        if result.matched_count > 0:
            print(f"'{company_name}' 문서가 덮어쓰기되었습니다.")
        else:
            print(f"'{company_name}' 새 문서가 삽입되었습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB 처리 중 오류 발생: {str(e)}")

    end_time = time.time()  # 요청 처리 완료 시간
    elapsed_time = end_time - start_time1  # 경과 시간 계산

    print(f"총 처리 시간: {elapsed_time:.2f}초")  # 소수점 두 자리까지 출력

    return {f"'{company_name}' dart_report MongoDB 저장 완료"}


# # Test3 - text_content 변수에 저장
# @router.post("/mongoTest/")
# async def get_files_by_corp_name1(corp_name: str):
#     cursor = db['fs.files'].find({"metadata.corp_name": corp_name})

#     text_content = ""  # 모든 텍스트 데이터를 저장할 변수
    
#     async for file_doc in cursor:
#         grid_out = await fs.open_download_stream(file_doc['_id'])
#         file_data = await grid_out.read()

#         try:
#             # base64 디코딩 후 utf-8 텍스트로 변환
#             decoded_data = file_data.decode('utf-8')
#             # 텍스트 데이터를 변수에 저장
#             text_content += decoded_data + "\n\n"  # 각 파일 데이터를 구분하기 위해 개행 추가
#         except Exception as e:
#             return {"status": "error", "message": str(e)}
            
#     cleaned_text = clean_text(text_content)
#     return {"status": "success", "message": cleaned_text}

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



