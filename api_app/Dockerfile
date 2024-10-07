# Python 3.12 공식 이미지를 기반으로 합니다
FROM python:3.12-slim

# 필수 패키지 업데이트 및 JDK 17 설치
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /api_app

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
#COPY ./app /api_app/app
COPY ./app ./app


# PYTHONPATH 설정
ENV PYTHONPATH=/api_app

# JAVA_HOME 설정
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# 포트 설정
EXPOSE 8000

# 애플리케이션 실행
#CMD ["python", "app/main.py"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
