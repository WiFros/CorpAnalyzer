from typing import Dict
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from schemas.langchain.news.news_schema import CompanySummary

import os


# schema = StructType([
#     StructField("title", StringType(), nullable=False),
#     StructField("embedding_vector", ArrayType(FloatType()), nullable=False)
# ])

# embedding_udf = udf(embedding, schema)


def news_summarization(company_name : str = "", documents : Dict = {})-> str:
    API_KEY = "AIzaSyBKpwmTbXLt6Y6Dc5NcVinepIW2fhCH7l4"
    os.environ["GOOGLE_API_KEY"] = API_KEY
    # make 
    request_data = ""
    for document in documents:
        request_data += " " + document["_source"]["description"]
    
    # make request to google GEN AI, 매개변수 다 yaml으로 빼기
    model = ChatGoogleGenerativeAI(model = "gemini-1.5-flash-latest")
    
    template ="""
    내가 준 Document 데이터로 Company의 기술 및 서비스의 최신 동향 TOP5로 요약해줘.
    Document : {document}

    Company : {company}

    Format : {format}
    """
    parser = PydanticOutputParser(pydantic_object= CompanySummary)

    prompt = PromptTemplate.from_template(template)
    formatted_prompt = prompt.format(document = documents, company = company_name, format = parser.get_format_instructions())

    message = HumanMessage(content=formatted_prompt)
    response = model([message])

    return response.__dict__['content']



