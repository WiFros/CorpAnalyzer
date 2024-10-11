다음은 제공된 요약과 PDF 내용을 바탕으로 한 프로젝트 README입니다.

---

# 기업 해체 분석기 - Six-Pack

## 프로젝트 설명
**기업 해체 분석기**는 DART 전자 공시 문서와 최신 뉴스 데이터를 분석하여 기업의 주요 정보를 제공하는 서비스입니다. 생성형 AI, Elasticsearch, 그리고 다양한 데이터 시각화 도구를 통해 기업 분석과 관련된 모든 정보를 통합하여 사용자에게 제공합니다. 이 서비스는 특히 취업 준비생이나 기업 분석을 필요로 하는 사람들에게 기업 현황, 최신 산업 트렌드, 재무 분석 등을 쉽고 빠르게 제공하는 것을 목표로 합니다.

## 주요 기능
1. **전자 공시 문서 요약**
   - DART에서 추출한 방대한 기업 공시 보고서를 분석하고, 기업 현황, 연구 및 계약 정보 등을 요약하여 시각적으로 제공합니다.

2. **뉴스 분석 및 트렌드 시각화**
   - Elasticsearch 기반의 뉴스 데이터 분석으로, 상위 500개의 뉴스 문서에서 가장 중요한 50개 문서를 추출하고 이를 요약하여 시각화합니다.
   - 기업당 100개의 뉴스를 분석하여 키워드 기반 트렌드 워드 클라우드를 생성하고, 최신 트렌드를 한눈에 파악할 수 있도록 시각화합니다.

3. **재무제표 시각화**
   - DART에서 제공하는 주요 재무제표 데이터를 크롤링하고 이를 시각화하여, 매출액 추이, 성장률, 수익성 지표 등을 제공합니다.

4. **뉴스 중복 제거**
   - BigBird Transformer 기반의 임베딩과 DBSCAN 군집화 알고리즘을 통해 뉴스 문서 중복을 30~50% 제거합니다.

5. **문서 요약 및 회사 이름 추출**
   - KoELECTRA 기반의 NER 모델로 뉴스 본문에서 기업 이름을 추출하고, Bart 모델을 이용하여 문서를 요약합니다.

## 기술 스택
- **Frontend**: React
- **Backend**: FastAPI
- **Database**: MongoDB, Elasticsearch, Hadoop
- **Infra**: Jenkins, Nginx, Docker, Airflow
- **Deep Learning**: Huggingface Transformers, Pytorch, Numpy, Pandas

## 설치 및 실행 방법
### 1. 환경 설정
   - Docker, docker-compose 설치 필수

   - 프로젝트 클론:
     ```bash
     git clone http://j11a606a.p.ssafy.io
     cd S11P21A606
     ```

### 2. 프로젝트 간단 실행(도커 사용)
   - Frontend 설치:
     ```bash
     cd front
     docker-compose up -d
     ```
   - Backend 설치:
     ```bash
     cd api_app
     docker-compose up -d
     ```
   - ES 실행

## 사용법
1. 웹 애플리케이션 실행 후, 기업 이름을 검색하여 관련 정보를 확인합니다.
2. DART 기반의 재무제표와 관련 뉴스 데이터를 통해 기업의 현재 상황과 트렌드를 시각적으로 파악할 수 있습니다.

## 기여 방법
- 이 프로젝트에 기여하고 싶으시면, Fork를 하신 후 Pull Request를 보내주시거나 이슈를 등록해주세요.
- 기여 전 `CONTRIBUTING.md` 파일을 참고해주세요.

## 라이센스
- 이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.

## 개발 팀
- **Frontend**: 홍수연
- **Backend**: 안재현, 김도훈, 이현재, 김세훈, 박정영
- **Infra**: 박정영, 김도훈

## 참고 자료
- [Open Dart API](https://dart.fss.or.kr)
- [Naver Finance API](https://finance.naver.com)

---

이 README는 프로젝트의 개요와 주요 기능을 포함하며, 기술 스택과 실행 방법을 제공하고 있습니다. 이를 통해 개발자들이 프로젝트를 이해하고, 기여할 수 있도록 돕습니다.
