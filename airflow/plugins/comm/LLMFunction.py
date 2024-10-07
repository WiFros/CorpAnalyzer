from datetime import datetime

import requests
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, ConnectionFailure

# host: str = "70.12.247.100:8081"
#host: str = "70.12.114.101:8081"
host: str = "218.235.71.63:8081"


def call_RAG_server() -> list[dict]:
    result: list[dict] = []

    with open('/usr/local/airflow/include/data.txt', 'r') as file:
        while True:
            corp_name: str = file.readline()

            if not corp_name:
                break

            response = requests.get(f"http://{host}/news", params={"company_name": corp_name})

            if response.status_code == 200:
                element = {"company_name": corp_name, "item": response.json()}
                result.append(element)

    return result


def store_to_mongo(**context):
    data: list[dict] = context['task_instance'].xcom_pull(task_ids='call_RAG')

    print(data)

    dataset: list[dict] = []
    for element in data:
        dataset.append(_transform(element['item'], element['company_name']))

    client = MongoClient("mongodb://admin:ssafya606@j11a606.p.ssafy.io:27017")
    database = client['company_db']
    collection = database['news_report']

    try:
        collection.insert_many(dataset, ordered=False)
    except BulkWriteError as e:
        print(e.details)
    finally:
        client.close()

    print("success")

def _transform(result_data: dict, company_name: str) -> dict:
    return {
        "result": result_data,
        "company_name": company_name,
        "created_at": datetime.now()
    }

if __name__ == "__main__":
    client = MongoClient("mongodb://admin:ssafya606@j11a606.p.ssafy.io:27017")
    database = client['company_db']
    collection = database['news_report']

    try:
        client.admin.command('ping')
        print("success")
    except ConnectionFailure:
        print("error")