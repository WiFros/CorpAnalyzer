from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch, helpers
import yaml
import warnings

warnings.filterwarnings("ignore")


class ESClient:
    def __init__(self):
        with open("/usr/local/airflow/config.yaml", 'r') as configuration:
            props = yaml.load(configuration, Loader=yaml.FullLoader)

        try:
            self.client = Elasticsearch(
                hosts=props['elastic_search']['host'],
                verify_certs=False,
                basic_auth=(props['elastic_search']['id'], props['elastic_search']['password'])
            )

        except Exception as e:
            print("ES Client construction failed " + str(e))

    def bulk_index(self, index_name: str, docs: list[dict]) -> None:
        queries: list[dict] = []

        for doc in docs:
            operation = {
                "_index": index_name,
                "_source": {
                    "title": doc["title"],
                    "description": doc["description"],
                    "company_names": doc["company_names"],
                    "summary": doc["summary"],
                    "pubDate": doc["pubDate"],
                    "link": doc["link"]
                }
            }

            queries.append(operation)

        helpers.bulk(self.client, queries)

    def search(self, index_name: str, query: dict, size: int = 30) -> ObjectApiResponse[dict]:
        # index_name에서 query를 사용해 데이터 return
        resp = self.client.search(index=index_name,
                                  query=query,
                                  size=size)

        return resp

    def adv_search(self, index_name: str, body: dict) -> ObjectApiResponse[dict]:
        # index_name에서 body를 사용해 데이터 return
        resp = self.client.search(index=index_name, body=body)

        return resp

# if __name__ == '__main__':
#     client = ESClient()
#     res = client.search(index_name="test_index",
#                   query={"match":
#                                   {
#                                       "title": "외부에서 적재한 테스트 문서"
#                                    }
#                              })
#
#     print(res)
