from typing import Dict
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from schemas.langchain.news.news_schema import CompanySummary
from models.reranker import rerank_process
import os
import dotenv

dotenv.load_dotenv()
def news_summarization(company_name : str = "", documents : Dict = {})-> str:
    # API_KEY = 
    # os.environ["GOOGLE_API_KEY"] = API_KEY
    # select top 50 using rerank_process

    query = f"{company_name}의 기술과 미래 동향을 알려줘"
    request_data = ""
    if (len(documents) >=50):
        top_50_index = rerank_process(query, documents)
        for idx in top_50_index:
            request_data += " " + documents[idx]["_source"]["summary"]
    else:
        for idx in range(len(documents)):
            request_data += " " + documents[idx]["_source"]["summary"]
    
    model_name = os.getenv("GOOGLE_MODEL_NAME")

    # make request to google GEN AI, 매개변수 다 yaml으로 빼기
    model = ChatGoogleGenerativeAI(model = model_name,
                    timeout=None,
                    max_retries=10,
    )
    
    template ="""
    내가 준 Document 데이터로 Company의 기술 및 서비스의 최신 동향 TOP5로 요약해줘.
    Document : {document}

    Company : {company}

    Format : {format}
    """
    parser = PydanticOutputParser(pydantic_object= CompanySummary)

    prompt = PromptTemplate.from_template(template)
    formatted_prompt = prompt.format(document = request_data, company = company_name, format = parser.get_format_instructions())

    message = HumanMessage(content=formatted_prompt)
    response = model([message])

    return response.__dict__['content']



