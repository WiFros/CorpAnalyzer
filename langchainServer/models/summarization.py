from transformers import AutoTokenizer, AutoModelForTokenClassification \
    ,pipeline, logging
from typing import List
from schemas.summarization import SumResponse
from schemas.request import NewsItem
import warnings
import pandas as pd
import os
logging.set_verbosity_error()
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
# warning 무시
warnings.filterwarnings('ignore')

# summ = pipeline("summarization", model = "gangyeolkim/kobart-korean-summarizer-v2", device = "cuda")


def chunk_text(text, max_length = 1024):
    # 입력 텍스트를 1024로 truncated
    chunks = []
    for i in range(0, len(text), max_length):
        chunks.append(text[i:i + max_length])
    return chunks





# def summarization(text: DataFrame, spark: SparkSession = Depends(get_spark)) -> DataFrame:
#     # UDF를 사용하여 DataFrame의 각 행에 요약 적용
#     summ = pipeline("summarization", model = "gangyeolkim/kobart-korean-summarizer-v2", device = "cuda")

#     df_with_summary = text.withColumn("summary", summarize_udf(col("description")))
    
#     return df_with_summary


def summarization(text: pd.DataFrame) -> pd.DataFrame:
    import torch
    summ = pipeline("summarization", model = "gangyeolkim/kobart-korean-summarizer-v2", device = "cuda")

    summ_list = []
    for _, row in text.iterrows():
        chunks = chunk_text(row['description'])

        res = summ(chunks[0])[0]["summary_text"]
        # for chunk in chunks:
        #     if (len(chunk) > 10):
        #         res += summ(chunk)[0]["summary_text"]
        
        # if len(chunks) > 1:
        #     # 여러 청크를 요약한 후 다시 요약
        #     try : 
        #         res = summ(res)[0]["summary_text"]
        #     except:
        #         print(res)

        summ_list.append(res)
    torch.cuda.empty_cache()
    del summ
    # 2. pandas df에 새 칼럼 생성
    text["summary"] = summ_list

    return text   