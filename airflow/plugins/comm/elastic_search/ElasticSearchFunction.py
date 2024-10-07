from elastic_transport import ObjectApiResponse

from ElasticSearchClient import ESClient
import json
import pandas as pd

client: ESClient = ESClient()


def store_to_elastic_search(**context) -> None:
    data_list: list[dict] = context['task_instance'].xcom_pull(task_ids='summarization_processing')
    client.bulk_index("news_docs", data_list)


def get_news_from_elastic_search(company_name: str):
    result: ObjectApiResponse[dict] = client.search(
        index_name="news_docs",
        query={
            "match": {
                "company_names": company_name
            }
        }
    )

    print(json.dumps(result['hits']['hits'], indent=4, ensure_ascii=False))
