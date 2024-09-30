from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from typing import List, Dict
from schemas.request import NewsItem
from schemas.ner import NerResponse
from tqdm import tqdm
import gc
import pandas as pd






# def merge_entities(entities: List[Dict]) -> List[Dict]:
#     merged_entities = []
#     current_entity = ""
#     current_label = ""
#     current_score = 0
#     token_count = 0

#     for entity in entities:
#         word = entity['word']
#         label = entity['entity']
#         score = entity['score']

#         # Check for the beginning of an entity
#         if label.startswith("B-OG"):
#             if current_entity:
#                 merged_entities.append({
#                     "entity": current_entity,
#                     "label": current_label,
#                     "score": current_score / token_count  # Average score
#                 })
#             current_entity = word
#             current_label = label
#             current_score = score
#             token_count = 1
#         elif label.startswith("I-OG") and current_entity:
#             current_entity += word if not word.startswith("##") else word[2:]
#             current_score += score
#             token_count += 1
#         else:
#             if current_entity:
#                 merged_entities.append({
#                     "entity": current_entity,
#                     "label": current_label,
#                     "score": current_score / token_count
#                 })
#                 current_entity = ""
#                 current_label = ""
#                 current_score = 0
#                 token_count = 0

#     if current_entity:
#         merged_entities.append({
#             "entity": current_entity,
#             "label": current_label,
#             "score": current_score / token_count
#         })

#     return merged_entities

def merge_entities(entities):
    merged_entities = []
    current_entity = ""
    current_label = ""
    current_score = 0
    token_count = 0

    for entity in entities:
        word = entity['word']
        label = entity['entity']
        score = entity['score']

        # B-OG: 시작하는 새로운 엔터티
        if label.startswith("B-OG"):
            # 이전 엔터티가 있으면 저장
            if current_entity:
                merged_entities.append({
                    "entity": current_entity,
                    "label": current_label,
                    "score": current_score / token_count  # 평균 점수
                })
            # 새로운 엔터티 시작
            current_entity = word if not word.startswith("##") else word[2:]
            current_label = label
            current_score = score
            token_count = 1
        # I-OG: 같은 엔터티의 이어지는 토큰
        elif label.startswith("I-OG") and current_entity:
            # ##로 시작하면 이어 붙이기
            if word.startswith("##"):
                current_entity += word[2:]
            else:
                current_entity += " " + word
            current_score += score
            token_count += 1
        else:
            # 다른 엔터티나 구분되는 토큰일 경우, 현재 엔터티 저장
            if current_entity:
                merged_entities.append({
                    "entity": current_entity,
                    "label": current_label,
                    "score": current_score / token_count
                })
            # 엔터티 초기화
            current_entity = ""
            current_label = ""
            current_score = 0
            token_count = 0

    # 마지막 엔터티 추가
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

    for _, row in tqdm(text.iterrows(), total = len(text), desc = "NER Process"):
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

        