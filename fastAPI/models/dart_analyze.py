import pdfplumber
import re
import torch
from bs4 import BeautifulSoup
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

from schemas.dart_analyze import ReportSchema  # Pydantic 클래스 가져오기
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 텍스트 정제를 위한 함수
def clean_text(text):
    text = text.replace('|n', '')
    text = re.sub(r'\.{2,}', '.', text)
    return " ".join(text.split())

# HTML 파일을 처리하는 함수
async def process_html(file):
    # HTML 파일에서 텍스트 추출
    contents = await file.read()  # 비동기 작업 대기
    decoded_contents = contents.decode('utf-8')  # 바이트를 문자열로 변환
    soup = BeautifulSoup(decoded_contents, "html.parser")
    text = soup.get_text()
    cleaned_text = clean_text(text)
    return cleaned_text

# PDF 파일을 처리하는 함수
def process_pdf(file):
    docs = []
    with pdfplumber.open(file.file) as pdf:
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text()
            cleaned_text = clean_text(text)
            doc = Document(page_content=cleaned_text, metadata={"page": i})
            docs.append(doc)
    return docs

# 파일을 분석하는 함수 (PDF와 HTML 처리)
async def process_rag(file, company_name):
    # 파일 타입을 확인하여 PDF 또는 HTML로 처리
    docs = []
    if file.content_type == "application/pdf":
        # PDF 파일 처리
        docs = process_pdf(file)
    elif file.content_type == "text/html":
        # HTML 파일 처리
        html_content = await process_html(file)
        doc = Document(page_content=html_content, metadata={"file": file.filename})
        docs.append(doc)
    else:
        raise ValueError("지원하지 않는 파일 형식입니다. PDF 또는 HTML 파일만 지원됩니다.")

    # 문서 분할
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_documents = text_splitter.split_documents(docs)

    # GPU 장치 설정 - GPU 사용 시
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 임베딩 생성
    model_name = "intfloat/multilingual-e5-large-instruct"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"}, # GPU 설정해도 되는데 200청크 이내 cpu로 해도 큰 차이 없을 듯??(뇌피셜)
        encode_kwargs={"normalize_embeddings": True},
    )
    vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # 프롬프트 생성
    prompt = PromptTemplate.from_template(
        """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Answer in Korean.

        #Context: 
        {context}

        #Question:
        {question}

        #Answer:"""
    )

    # 언어모델 생성
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")

    # 체인 생성
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 여러 개의 질문을 정의하고 답변을 추출
    questions = [
        f"{company_name} 주요 사업 내용을 문서에서 찾아서 상세히 알려줘",
        f"{company_name} 주요 제품 및 서비스 매출을 상세히 알려줘",
        f"{company_name} 주요 계약 및 연구개발활동을 상세히 알려줘"
    ]

    results = []
    for question in questions:
        response = chain.invoke(question)
        results.append({"question": question, "answer": response})

    # 항목별로 딕셔너리 생성하여 반환
    report = ReportSchema(
        company_name=company_name,
        business_overview=results[0]['answer'],
        products_and_sales=results[1]['answer'],
        contracts_and_rnd=results[2]['answer']
    )

    return report