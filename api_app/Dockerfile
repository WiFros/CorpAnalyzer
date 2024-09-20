# Python 3.12 공식 이미지를 기반으로 합니다
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /api_app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY ./app /api_app/app

# PYTHONPATH 설정
ENV PYTHONPATH=/api_app

# 포트 설정
EXPOSE 8000

# 애플리케이션 실행
CMD ["python", "app/main.py"]