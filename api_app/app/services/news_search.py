import logging
from elasticsearch import AsyncElasticsearch
from typing import List, Dict, Any

class NewsSearchService:
    def __init__(self):
        self.db = AsyncElasticsearch(
            hosts="https://j11a606.p.ssafy.io:9200",
            verify_certs=False,
            basic_auth=('elastic', 'ssafya606')
        )

    async def search_news(self, company_name: str, size: int = 10) -> List[Dict[str, Any]]:
        logging.info(f"Searching news for company: {company_name}, size: {size}")
        query = {
            "query": {
                "match": {
                    "company_names": company_name
                }
            },
            "size": size,
            "min_score": 1.5,
        }
        try:
            result = await self.db.search(index="news_docs", body=query)
            logging.info(f"Elasticsearch raw result: {result}")  # 전체 ES 결과를 로깅
            hits = result.get("hits", {}).get("hits", [])
            logging.info(f"Extracted hits: {hits}")  # 추출된 hits를 로깅
            return [{"_id": hit["_id"], "_source": hit["_source"]} for hit in hits]
        except Exception as e:
            logging.error(f"Error during news search: {str(e)}", exc_info=True)
            return []