import requests
import json
from hdfs import InsecureClient

#domain: str = "70.12.247.100:8080"
#domain: str = "70.12.114.101:8080"
# domain: str = "218.235.71.63:8080"
domain: str= "host.docker.internal:8081"

def embedding_processing(**context):
    collected_data: list[dict] = context['task_instance'].xcom_pull(task_ids='collecting_data')

    # request to fast api gpu server
    request_url: str = f'http://{domain}/embedding'
    response = requests.post(url=request_url, json=collected_data[:10])

    if response.status_code != 200:
        raise Exception(response.status_code, response.json())

    result = response.json()['data']
    print(type(result))

    return result


def ner_processing(**context):
    embedding_data: list = context['task_instance'].xcom_pull(task_ids='embedding_processing')

    # request to fast api gpu server
    request_url: str = f'http://{domain}/ner'
    response = requests.post(url=request_url, json=embedding_data)

    if response.status_code != 200:
        raise Exception(response.status_code, response.json())

    return response.json()['data']


def summarization_processing(**context):
    ner_data: list = context['task_instance'].xcom_pull(task_ids='ner_processing')

    # request to fast api gpu server
    request_url: str = f'http://{domain}/summarize'
    response = requests.post(url=request_url, json=ner_data)

    if response.status_code != 200:
        raise Exception(response.status_code, response.json())

    return response.json()['data']


def store_to_hadoop(**context) -> None:
    # data_list: list[dict] = context['task_instance'].xcom_pull(task_ids='summarization_processing')
    # #하둡
    # hadoop_client = InsecureClient('http://j11a606a.p.ssafy.io:9870', user='hadoop')

    # for data in data_list:
    #     company_name = data["company_names"]
    #     date = data["pubDate"]
    #     hdfs_file_path = f'/data/news/{company_name}/{date}/{company_name}.json'

    #     # 하둡 저장
    #     json_data = json.dumps(data, indent=4, ensure_ascii=False)
            
    #     with hadoop_client.write(hdfs_file_path, encoding='utf-8', overwrite=True) as writer:
    #         writer.write(json_data)
    pass
