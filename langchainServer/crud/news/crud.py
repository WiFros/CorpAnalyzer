import json
from data.mongodbclient import collection

def item_helper(item) -> dict:
    return {
        "company_name": item["company_name"],
        "result": item.get("result"),
        "created_at": item["created_at"]
    }


# 데이터 삽입
async def create_result(result_data: str) -> dict:

    result = await collection.insert_one(result_data)
    return str(result.inserted_id)

# 모든 항목 가져오기
async def get_all_items():
    items = []
    async for item in collection.find():
        items.append(item_helper(item))
    return items

# 특정 항목 가져오기
async def get_item_by_company_name(company_name: str) -> dict:
    # MongoDB에서 데이터를 가져옴
    news = await collection.find_one({"company_name": company_name})
    if news:
        return item_helper(news)
    return None