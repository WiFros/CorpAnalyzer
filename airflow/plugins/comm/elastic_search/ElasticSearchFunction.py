from elastic_transport import ObjectApiResponse
from transformers import AutoModel, AutoTokenizer
from ElasticSearchClient import ESClient
import json
import torch
import pandas as pd

model_name = "monologg/kobigbird-bert-base"
client: ESClient = ESClient()
index_name : str = "news_embedding"
size = 500

def store_to_elastic_search(**context) -> None:

    data_list: list[dict] = context['task_instance'].xcom_pull(task_ids='summarization_processing')
    client.bulk_index(index_name, data_list)


def get_news_from_elastic_search(company_name: str):

    model = AutoModel.from_pretrained(model_name).half()  # BigBirdModel
    tokenizer = AutoTokenizer.from_pretrained(model_name)  # BertTokenizer

    query_sent = f"{company_name}의 기술과 미래 동향을 알려줘"

    inputs = tokenizer(query_sent, return_tensors='pt', padding=True, truncation=True, max_length=4096)
        
    # 모델을 통해 추론
    with torch.no_grad():  # 그래디언트 계산 비활성화
        outputs = model(**inputs)
        outputs= outputs.last_hidden_state.mean(dim = 1)
        outputs = torch.nn.functional.normalize(outputs, p= 2, dim = -1)
        outputs = outputs.to('cpu')
    # 결과에서 필요한 부분을 추출 (예: 마지막 은닉 상태)
    torch.cuda.empty_cache()
    outputs = outputs.detach().numpy()[0]
    output = outputs.tolist()

    body = {
    "size": size,
    "query": {
        "bool": {
        "must": [
            {
            "knn" : {
                "field": "embedding_vector",
                "query_vector":output,
                "k": 10000,
            }
            },
            {
            "match": {
                "company_names": f"{company_name}"
            }
            }
        ]
        }
    }
    }
    result : ObjectApiResponse[dict] = client.adv_search(
        index_name=index_name,
        body=body
    )
    # result: ObjectApiResponse[dict] = client.search(
    #     index_name= index_name,
    #     query={
    #         "match": {
    #             "company_names": company_name
    #         }
    #     }
    # )

    print(json.dumps(result['hits']['hits'], indent=4, ensure_ascii=False))
