import dart_fss as dart
import json
from datetime import datetime

# DART OpenAPI 키 설정
API_KEY = "544481154425a2e397814d0b2156ab67a5c0ee61"

def get_company_list():
    # DART OpenAPI 초기화
    dart.set_api_key(API_KEY)
    
    # 모든 상장회사 정보 가져오기
    corp_list = dart.get_corp_list()
    
    # 회사 정보를 딕셔너리 리스트로 변환
    companies = []
    for corp in corp_list:
        company_info = {
            "corp_code": corp.corp_code,
            "corp_name": corp.corp_name,
            "stock_code": corp.stock_code,
            "modify_date": corp.modify_date  # modify_date는 이미 문자열 형태입니다.
        }
        companies.append(company_info)
    
    return companies

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    try:
        companies = get_company_list()
        if companies:
            filename = f"company_list_{datetime.now().strftime('%Y%m%d')}.json"
            save_to_json(companies, filename)
            print(f"{len(companies)}개의 회사 정보가 {filename}에 저장되었습니다.")
        else:
            print("회사 리스트를 가져오는데 실패했습니다.")
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    main()
