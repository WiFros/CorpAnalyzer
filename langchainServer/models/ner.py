from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from typing import List, Dict
from schemas.request import NewsItem
from schemas.ner import NerResponse
from pyspark.sql import SparkSession,DataFrame
from pyspark.sql.types import StructType, StructField,ArrayType, StringType
from pyspark.sql.functions import col, udf
from fastapi import Depends
import gc
import pandas as pd






def merge_entities(entities: List[Dict]) -> List[Dict]:
    merged_entities = []
    current_entity = ""
    current_label = ""
    current_score = 0
    token_count = 0

    for entity in entities:
        word = entity['word']
        label = entity['entity']
        score = entity['score']

        # Check for the beginning of an entity
        if label.startswith("B-OG"):
            if current_entity:
                merged_entities.append({
                    "entity": current_entity,
                    "label": current_label,
                    "score": current_score / token_count  # Average score
                })
            current_entity = word
            current_label = label
            current_score = score
            token_count = 1
        elif label.startswith("I-OG") and current_entity:
            current_entity += word if not word.startswith("##") else word[2:]
            current_score += score
            token_count += 1
        else:
            if current_entity:
                merged_entities.append({
                    "entity": current_entity,
                    "label": current_label,
                    "score": current_score / token_count
                })
                current_entity = ""
                current_label = ""
                current_score = 0
                token_count = 0

    if current_entity:
        merged_entities.append({
            "entity": current_entity,
            "label": current_label,
            "score": current_score / token_count
        })

    return merged_entities


def ner(text: pd.DataFrame)-> pd.DataFrame:
    import torch
    tokenizer = AutoTokenizer.from_pretrained("Leo97/KoELECTRA-small-v3-modu-ner")
    model = AutoModelForTokenClassification.from_pretrained("Leo97/KoELECTRA-small-v3-modu-ner")
    ner_pipeline = pipeline("ner", model = model, tokenizer = tokenizer, device = "cuda")

    company_names = []

    for _, row in text.iterrows():
        entities = ner_pipeline(row['description'])
        cand = []
        in_text_company_names = []

        for entity in entities:
            if "B-OG" in entity['entity']:
                if len(cand) != 0:
                    # 엔티티 병합
                    interm = merge_entities(cand)
                    if len(interm) != 0:
                        in_text_company_names.append(interm[0]["entity"])
                    cand = []
                cand.append(entity)
            elif "I-OG" in entity['entity']:
                cand.append(entity)
        
        if cand:
            interm = merge_entities(cand)
            if len(interm) != 0:
                in_text_company_names.append(interm[0]["entity"])
            
        company_names.append(in_text_company_names)

    text['company_names'] = company_names
    del ner_pipeline
    torch.cuda.empty_cache()
    return text

        