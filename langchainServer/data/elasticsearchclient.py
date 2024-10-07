from elasticsearch import Elasticsearch, helpers
from typing import Dict
from schemas.elasticsearch.request import NewsESSchema
from schemas.summarization import SumResponse
from pydantic import ValidationError

class ESclient:
    # ElasticSearch client not fit with data

    def __init__(self,path= None):
        if (path is None):
            self.client = Elasticsearch("http://localhost:9200")
        else :
            self.client = Elasticsearch(
                hosts="https://j11a606.p.ssafy.io:9200",
                verify_certs=False,
                basic_auth=("elastic", "ssafya606")
            )

    def get_info(self,):
        return self.client.info()
    
        
    def index_docs(self, index_name ,docs):
        # Create도 됨.
        
        valid_list = []
        
        for doc in docs:
    
            valid_list.append(doc.dict())

        
        if valid_list:
            self.bulk_index(index_name,valid_list)
        
        return {
            "indexed_count": len(valid_list),
        }
    
    def bulk_index(self, index_name ,docs):

        queries = []
        for doc in docs:
            operation = {
                        "_index": index_name,
                        "_source" : {
                            "title" : doc["title"],
                            "description" : doc["description"],
                            "company_names" : doc["company_names"],
                            "summary" : doc["summary"],
                            "published_date" : doc["published_date"],
                            "link" : doc["link"]

                        }
            }
            queries.append(operation)

        helpers.bulk(self.client,queries)

    def search(self, index_name, query,size = 30):
        # index_name에서 query를 사용해 데이터 return
        resp = self.client.search(index = index_name,
                                  query = query,
                                  size = size,
                                  )
        
        return resp
    
    def adv_search(self, index_name, body):
    # index_name에서 body를 사용해 데이터 return
        resp = self.client.search(index = index_name,
                                body = body)
    
        return resp


    


    