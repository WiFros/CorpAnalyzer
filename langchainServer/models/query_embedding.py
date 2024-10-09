from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from typing import Dict, List
from transformers import AutoModel, AutoTokenizer
from tqdm import tqdm
import pandas as pd
import numpy as np
import faiss 
import json
import torch
import dotenv
import os

def exp_normalize(x):
    b = x.max() 
    y = np.exp(x - b)
    return y / y.sum()


def embedding_process(company_name):
    model_name = os.getenv("EMBEDDING_MODEL_NAME")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
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
    model.to('cpu')
    del model
    torch.cuda.empty_cache()
    return output
