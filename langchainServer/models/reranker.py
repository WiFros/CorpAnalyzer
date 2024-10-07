from elasticsearchclient import ESclient
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from typing import Dict, List
from transformers import AutoModel, AutoTokenizer,AutoModelForSequenceClassification
from tqdm import tqdm
import pandas as pd
import numpy as np
import faiss 
import json
import torch


def exp_normalize(x):
    b = x.max() 
    y = np.exp(x - b)
    return y / y.sum()


def rerank_process(query, document):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained("Dongjin-kr/ko-reranker")
    model = AutoModelForSequenceClassification.from_pretrained("Dongjin-kr/ko-reranker").to(device).half()
    
    pairs = [[query, document[idx]["_source"]["summary"]] for idx in range(len(document))]

    # 상위 100개 문서를 reranker로 점수 매기기.
    scores = []
    for pair in tqdm(pairs, total = len(pairs) ,desc = "rerank process"):
        with torch.no_grad():
            inputs=  tokenizer([pair], padding= True, truncation = True, return_tensors= 'pt' , max_length = 512).to(device)
            score = model(**inputs, return_dict = True).logits.view(-1,).float()
            inputs.to('cpu')
            torch.cuda.empty_cache()

        scores.append(score[0].to('cpu').numpy())
    array = np.array(scores)
    
    top_50_indices = np.argsort(array)[-50:][::-1]  # 내림차순으로 상위 50개
    
    model.to('cpu')
    del model
    torch.cuda.empty_cache()
    return top_50_indices
