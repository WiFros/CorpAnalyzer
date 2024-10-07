from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.mongo import get_collection
from hdfs import InsecureClient
from bson import ObjectId
from datetime import datetime
import json

class NewsSummaryService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def get_summary_news_from_mongo(self, company_name: str):

        company_cursor = self.db.news_report.find({"company_name": company_name})

        # 데이터를 리스트로 변환하여 결과 받기
        companies = await company_cursor.to_list(length=100)  # 최대 100개의 결과 가져오기

        if companies:
            return companies
        return None

    async def get_summary_news_from_hadoop(self, company_name: str):
        client = InsecureClient('http://j11a606a.p.ssafy.io:9870', user='hadoop')
        hdfs_file_path = f'/news/{company_name}/{company_name}.json'

        try:
            # HDFS 파일을 읽기 모드로 열기
            with client.read(hdfs_file_path, encoding='utf-8') as reader:
                json_data = reader.read()
                # JSON 데이터 파싱
                company_data = json.loads(json_data)
                return company_data

        except Exception as e:
            print(f"Error reading from HDFS: {e}")

        return None

    @staticmethod
    def json_serializer(obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 string
        raise TypeError(f"Type {type(obj)} is not serializable")
    async def save_all_summary_news_from_mongo_to_hadoop(self):

        company_cursor = self.db.news_report.find({})

        # 데이터를 리스트로 변환하여 결과 받기
        result = await company_cursor.to_list(length=500)  # 최대 100개의 결과 가져오기

        if result:
            client = InsecureClient('http://j11a606a.p.ssafy.io:9870', user='hadoop')
            for company in result:
                company_name = company['company_name'].strip()
                json_data = json.dumps(company, indent=4, ensure_ascii=False, default=self.json_serializer)
                hdfs_file_path = f'/news/{company_name}/{company_name}.json'
                with open('temp.json', 'w', encoding='utf-8') as temp_file:
                    temp_file.write(json_data)

                # 업로드 및 덮어쓰기
                client.upload(hdfs_file_path, 'temp.json', overwrite=True)
        return None