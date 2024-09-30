from transformers import AutoTokenizer, AutoModelForTokenClassification,AutoModel ,pipeline
from typing import List, Tuple
from langchain_huggingface import HuggingFaceEmbeddings
from schemas.request import NewsItem, NewsBatchRequest
from schemas.embedding import EmbeddingResponse, EmbeddingBatchResponse
from sklearn.cluster import DBSCAN
from tqdm import tqdm
import numpy as np 
import pandas as pd
import gc
import json
import faiss


# schema = StructType([
#     StructField("title", StringType(), nullable=False),
#     StructField("embedding_vector", ArrayType(FloatType()), nullable=False)
# ])

# embedding_udf = udf(embedding, schema)


def dedup(text: pd.DataFrame)->pd.DataFrame:
    import torch

    # df_dedup = text.withColumn("embeddings", embedding_udf(col("title")))
    # model_name = "intfloat/multilingual-e5-large-instruct"
    model_name = "monologg/kobigbird-bert-base"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to('cuda').half()

    print("before dedup" , text.shape[0])
    embeddings_list = []
    for _, row in tqdm(text.iterrows(), total = len(text) , desc = "dedup"):
        with torch.no_grad():
            inputs = tokenizer(row['description'], return_tensors= 'pt',  # 최대 길이 설정
    truncation=True).to('cuda')
            output = model(**inputs).last_hidden_state
            output = torch.nn.functional.normalize(output,p=2,dim=2).mean(1)
        embeddings_list.append(output.detach().cpu().numpy().tolist()[0])
        torch.cuda.empty_cache()

    model.to("cpu")
    torch.cuda.empty_cache()
    del model
    # step 1 : ANN으로 중복제거
    # dim = len(embeddings_list[0])
    # index= faiss.IndexFlatL2(dim)
    # index.add(np.array(embeddings_list))

    # num_neighbor = 5 # k-nn 에서 k 선택
    


    # embeddings_list = df_dedup.select("embeddings").rdd.flatMap(lambda x: x).collect()



    # stpe 2 : DBSCAN으로 확실하게 중복제거.
    # dbsc = DBSCAN(eps=0.2, min_samples=1).fit(embeddings_list)
    dbsc = DBSCAN(eps=0.08, min_samples=1).fit(embeddings_list)
    labels = dbsc.labels_
    deduped_rows = []
    all_duped_art = []
    for label in set(labels):
        duped_rows = []
        dup_index = np.where(labels == label)[0]
        first_index = dup_index[0]  # 첫 번째 인덱스
        # 나머지 중복 인덱스 저장.
        for idx in dup_index:
            article_data = text.iloc[idx].to_dict()
            article_data = {k: (v.item() if isinstance(v, np.generic) else v) for k, v in article_data.items()}
            duped_rows.append(article_data)


        deduped_rows.append(text.iloc[first_index,:].to_list())

        all_duped_art.append({
            "label" : int(label),
            "articles" : duped_rows
        })

    print("after dedup" , len(deduped_rows))
    with open('duplicated_articles.json','w', encoding='utf-8') as j:
        json.dump(all_duped_art,j, ensure_ascii=False, indent = 4)
    if deduped_rows:  # 빈 리스트 체크
        df_res = pd.DataFrame(deduped_rows, columns= text.columns.tolist())
    else:
        df_res = pd.DataFrame([], columns= text.columns.tolist())
    
    return df_res



