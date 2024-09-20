FROM nvcr.io/nvidia/pytorch:24.01-py3

WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY ./app /app/app

# 포트 8001 노출
EXPOSE 8001

# FastAPI 애플리케이션 실행
CMD ["python", "app/main.py"]