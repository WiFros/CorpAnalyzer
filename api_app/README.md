# FastAPI 프로젝트 환경 설정 가이드 (Python 3.12, Windows, PyCharm)

이 가이드는 Windows 환경에서 Python 3.12, FastAPI, 그리고 PyCharm을 사용하여 프로젝트 환경을 설정하는 방법을 설명합니다.

## 필요 사항

- Python 3.12
- pip (Python 패키지 관리자)
- PyCharm (Community 또는 Professional 버전)

## 단계별 가이드

1. Python 3.12 설치
   - 공식 Python 웹사이트(https://www.python.org/downloads/)에서 Python 3.12를 다운로드하고 설치합니다.
   - 설치 중 "Add Python 3.12 to PATH" 옵션을 선택하세요.

2. Python 설치 확인
   - 명령 프롬프트(cmd)를 열고 다음 명령어를 실행합니다:
     ```
     python --version
     ```
   - Python 3.12.x가 출력되어야 합니다.

3. 프로젝트 디렉토리로 이동
   ```
   cd api_app
   ```

4. 가상 환경 생성
   ```
   python -m venv venv
   ```

5. FastAPI 및 의존성 설치
   - 가상 환경을 활성화합니다:
     ```
     venv\Scripts\activate
     ```
   - FastAPI를 설치합니다:
     ```
     pip install fastapi[standard]
     ```
6. PyCharm에서 프로젝트 열기
   - PyCharm을 실행하고 "Open" 옵션을 선택합니다.
   - 생성한 `api_app` 폴더를 선택하여 엽니다.

7. PyCharm 인터프리터 설정
   - File > Settings (또는 PyCharm > Preferences - Mac의 경우)로 이동합니다.
   - Project: fastapi-project > Python Interpreter를 선택합니다.
   - 인터프리터 설정 옆의 기어 아이콘을 클릭하고 "Add"를 선택합니다.
   - "Virtualenv Environment"를 선택합니다.
   - "Existing environment"를 선택하고, 인터프리터 경로를 프로젝트의 venv 폴더 내 Python 실행 파일로 지정합니다:
     - Windows: `[프로젝트 경로]\venv\Scripts\python.exe`
   - "OK"를 클릭하여 설정을 저장합니다.

8. 앱 실행
    - PyCharm 터미널에서 다음 명령어를 실행합니다:
      ```
      uvicorn main:app --reload
      ```

## 추가 참고사항

- 프로젝트에 새로운 패키지를 추가할 때마다 `requirements.txt` 파일을 업데이트하세요.
- PyCharm의 실행 구성을 설정하여 더 쉽게 FastAPI 앱을 실행할 수 있습니다:
  1. 상단 메뉴에서 "Run" > "Edit Configurations"를 선택합니다.
  2. "+" 버튼을 클릭하고 "Python"을 선택합니다.
  3. 이름을 "FastAPI"로 지정합니다.
  4. Script path에 uvicorn의 경로를 입력합니다: `[프로젝트 경로]\venv\Scripts\uvicorn.exe`
  5. Parameters에 `main:app --reload`를 입력합니다.
  6. Working directory를 프로젝트 루트 폴더로 설정합니다.
  7. "Apply" 및 "OK"를 클릭하여 저장합니다.

이제 실행 버튼을 클릭하여 FastAPI 앱을 쉽게 실행할 수 있습니다.