

from elasticsearch import Elasticsearch
class NewsLinkService:
    def __init__(self, company_name: str):
        self.db = Elasticsearch(
            hosts="https://j11a606.p.ssafy.io:9200",
            verify_certs=False,
            basic_auth=('elastic', 'ssafya606')
        )
        self.query = {
             "query": {
                "match": {
                    "company_names": f"{company_name}"
                }
              },
            "collapse": {
                "field": "title.keyword"  # 중복을 피할 필드
            },
              "sort": [
                {
                   "pubDate.keyword": {
                    "order": "desc"
                  }
                }
              ],
              "size": 5
        }

    async def get_news_link(self):
        results = self.db.search(index="news_docs", body=self.query)
        result = []
        for i in range(len(results['hits']['hits'])):

            result.append({
                'title':results['hits']['hits'][i]["_source"]['title'],
                'link':results['hits']['hits'][i]["_source"]['link']
            })

        return result