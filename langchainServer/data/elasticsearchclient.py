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
            self.client = Elasticsearch(path)
        self.schmeas = {
            "news_docs": SumResponse
        }

    def get_info(self,):
        return self.client.info()
    
    def validate_data(self, index_name, data):

        sc_class= self.schmeas.get(index_name)
        if not sc_class:
            raise ValueError(f"Index {index_name} doesn't exist")

        try:
            # Pydantic을 이용해 검증
            if isinstance(data, sc_class):
                return True, data
            
            sc_class(**data)
            return True, data
        except ValidationError as e:
            # print(f"Validation error: {e}")
            return False, data
        
    def index_docs(self, index_name ,docs):
        # Create도 됨.
        
        valid_list = []
        invalid_list = []

        for doc in docs:
            is_valid, doc = self.validate_data(index_name,doc)

            if is_valid:
                valid_list.append(doc.dict())
            else :
                invalid_list.append(doc.dict())
        
        if valid_list:
            self.bulk_index(index_name,valid_list)
        
        return {
            "indexed_count": len(valid_list),
            "invalid_count": len(invalid_list),
            "invalid_data": invalid_list
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
                            "pubDate" : doc["pubDate"],
                            "link" : doc["link"]

                        }
            }
            queries.append(operation)

        helpers.bulk(self.client,queries)



    