from transformers import AutoTokenizer, AutoModelForSeq2SeqLM \
    ,pipeline, logging
from typing import List
from schemas.summarization import SumResponse
from schemas.request import NewsItem
from tqdm import tqdm
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


# def summarization(text: pd.DataFrame) -> pd.DataFrame:
#     import torch
#     summ = pipeline("summarization", model = "gangyeolkim/kobart-korean-summarizer-v2", device = "cuda")

#     summ_list = []
#     for _, row in text.iterrows():
#         chunks = chunk_text(row['description'])

#         res = summ(chunks[0])[0]["summary_text"]
#         # for chunk in chunks:
#         #     if (len(chunk) > 10):
#         #         res += summ(chunk)[0]["summary_text"]
        
#         # if len(chunks) > 1:
#         #     # 여러 청크를 요약한 후 다시 요약
#         #     try : 
#         #         res = summ(res)[0]["summary_text"]
#         #     except:
#         #         print(res)

#         summ_list.append(res)
#     torch.cuda.empty_cache()
#     del summ
#     # 2. pandas df에 새 칼럼 생성
#     text["summary"] = summ_list

#     return text   

def summarization(text: pd.DataFrame) -> pd.DataFrame:
    import torch
    model_name = "EbanLee/kobart-summary-v3"
    # model_name = "gangyeolkim/kobart-korean-summarizer-v2"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device).half()
    summaries = []

# tqdm을 사용하여 진행 상황을 표시하며 각 기사를 요약
    for index, row in tqdm(text.iterrows(), total=len(text), desc="Summarizing articles"):
        # 기사 텍스트 가져오기
        article_text = row['description']
        
        # 토크나이징 및 GPU로 이동
        input_ids = tokenizer(article_text, return_tensors='pt', padding=True, truncation=True, max_length=1024).to(device)

        # 요약 생성
        with torch.no_grad():
            summary_ids = model.generate(
            input_ids=input_ids['input_ids'],
            attention_mask=input_ids['attention_mask'],
            bos_token_id=model.config.bos_token_id,
            eos_token_id=model.config.eos_token_id,
            length_penalty=1.0,
            max_length=300,
            min_length=12,
            num_beams=1,
            repetition_penalty=1.5,
            no_repeat_ngram_size=15,
            )
        torch.cuda.empty_cache()
        # 디코딩하여 요약 결과 저장
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)



    torch.cuda.empty_cache()
    del summ
    # 2. pandas df에 새 칼럼 생성
    text["summary"] = summaries

    return text   