# app/services/company_search.py

from app.utils.optimized_search import OptimizedSearch
from app.models.company import Company
from motor.motor_asyncio import AsyncIOMotorDatabase
from cachetools import TTLCache
from elasticsearch import Elasticsearch
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd
import asyncio


class hotKeywordService:
    def __init__(self,corp_name : str):

        self.db = Elasticsearch(
                hosts="https://j11a606.p.ssafy.io:9200",
                verify_certs=False,
                basic_auth=('elastic', 'ssafya606')
            )
        self.query = {
                "query" :{
                            "match" : {
                        "company_names" : f"{corp_name}"
                    }
                },
                "size" : 100, # 최대 가져오는 뉴스 수
                "min_score" : 1.5, # 스코어 필터링
            }
        self.corp_name = corp_name
        self.stop_words=  pd.read_csv('./stopwords.txt', header = None)[0].tolist()
        self.nori = Okt()
        self.embed = TfidfVectorizer(stop_words= self.stop_words)

    async def fetch_hotkeyword(self):

        result = self.db.search(index = "news_docs",
                                body = self.query)
        
        documents = []
        length = len(result['hits']['hits'])
        for idx in range(length):
            documents.append(result['hits']['hits'][idx]["_source"])
        
        df = pd.DataFrame(documents)
        df['tokenizer'] = df['description'].apply(self.preprocess_text)
        
        res = self.embed.fit_transform(df['tokenizer'])

        # TF-IDF 점수를 DataFrame으로 변환
        tfidf_df = pd.DataFrame(res.toarray(), columns=self.embed.get_feature_names_out())

        # 각 단어의 TF-IDF 점수 합계 계산
        tfidf_sum = tfidf_df.sum(axis=0)

        # TF-IDF 점수 기준으로 정렬하여 가장 높은 점수를 가진 단어 추출
        top_n = 20  # 원하는 상위 N개 단어 수
        top_words = tfidf_sum.nlargest(top_n)
        top_words_list = [word for word in top_words.index]

        return {
        "corp_name": self.corp_name,
        "keywords": top_words_list
        }
    
    def preprocess_text(self,text : str = ""):
        return ' '.join(self.nori.nouns(text))