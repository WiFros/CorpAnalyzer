import requests

domain: str = "70.12.247.100:8080"


def embedding_processing(**context):
    collected_data: list[dict] = context['task_instance'].xcom_pull(task_ids='collecting_data')

    # request to fast api gpu server
    request_url: str = f'http://{domain}/embedding'
    response = requests.post(url=request_url, json=collected_data)

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
    pass
