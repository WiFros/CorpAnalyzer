import json
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

# MongoDB 연결 정보
MONGO_URI = "mongodb://localhost:27017/"  # MongoDB 서버 URI
DB_NAME = "company_db"  # 데이터베이스 이름
COLLECTION_NAME = "companies"  # 컬렉션 이름

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def insert_to_mongodb(data):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # 기존 데이터 삭제 (선택사항)
    collection.delete_many({})

    try:
        # 벌크 삽입 수행
        result = collection.insert_many(data, ordered=False)
        print(f"성공적으로 {len(result.inserted_ids)}개의 문서를 삽입했습니다.")
    except BulkWriteError as bwe:
        # 일부 문서 삽입 실패 시 처리
        print(f"일부 문서 삽입 실패: {bwe.details['nInserted']}개 삽입, {len(bwe.details['writeErrors'])}개 실패")
    finally:
        client.close()

def main():
    json_file_path = "company_list_20240930.json"  # JSON 파일 경로
    
    # JSON 데이터 로드
    company_data = load_json_data(json_file_path)
    
    # MongoDB에 데이터 삽입
    insert_to_mongodb(company_data)

if __name__ == "__main__":
    main()
