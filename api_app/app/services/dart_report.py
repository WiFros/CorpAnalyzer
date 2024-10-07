from motor.motor_asyncio import AsyncIOMotorCollection

from fastapi import Depends, HTTPException

class DartReportService:
    def __init__(self, dart_collection: AsyncIOMotorCollection):
        self.dart_collection = dart_collection  # 컬렉션만 있으면 가능

    async def get_dart_report(self, company_name: str):
        try:
            # 회사 이름으로 문서 조회
            dart_report = await self.dart_collection.find_one({"company_name": company_name})

            if dart_report is not None:
                dart_report["_id"] = str(dart_report["_id"])  # ObjectId를 문자열로 변환
                return dart_report
            else:
                raise ValueError(f"'{company_name}'에 해당하는 데이터를 찾을 수 없습니다.")
        except Exception as e:
            raise ValueError(f"MongoDB에서 데이터를 가져오는 중 오류 발생: {str(e)}")
