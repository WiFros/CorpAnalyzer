# app/services/hotKeyword_search.py

import os
from pathlib import Path
from elasticsearch import Elasticsearch
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import pandas as pd


class hotKeywordService:
    def __init__(self, corp_name: str):
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
                    "collapse":{
                "field": "title.keyword"
            },
                "size" : 100, # 최대 가져오는 뉴스 수
                "min_score" : 1.5, # 스코어 필터링
            }
        self.corp_name = corp_name

        # stopwords.txt 파일 경로 설정
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent  # app 디렉토리로 이동
        stopwords_path = project_root / 'stopwords.txt'

        print(f"Current working directory: {os.getcwd()}")
        print(f"Attempting to read stopwords from: {stopwords_path}")

        if stopwords_path.exists():
            self.stop_words = pd.read_csv(stopwords_path, header=None)[0].tolist()
        else:
            print(f"Warning: stopwords.txt not found at {stopwords_path}")
            self.stop_words = []  # 또는 기본 불용어 목록 사용

        self.nori = Okt()
        self.embed = TfidfVectorizer(stop_words=self.stop_words)

    async def fetch_hotkeyword(self):

        result = self.db.search(index = "news_embedding",
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
    
    async def fetch_hotkeyword_with_news(self):

        result = self.db.search(index = "news_embedding",
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

        all_list = {}
        for word in top_words.index:
            cand = []
            for _,row in df.iterrows():
                if word in row['tokenizer']:
                    cand.append({
                        'title' : row.title,
                        'pubDate' : row.pubDate,
                        'link' : row.link
                    })
            cand_sorted = sorted(cand, key=lambda x: datetime.strptime(x['pubDate'], '%a, %d %b %Y %H:%M:%S %z'), reverse = True)
            all_list[word] = cand_sorted[:5]

        return all_list
    
    def preprocess_text(self,text : str = ""):
        return ' '.join(self.nori.nouns(text))