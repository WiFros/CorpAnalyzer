import json

from schemas.langchain.news.news_schema import CompanySummary

def company_summary_to_json(company_summary : CompanySummary):
    try:
        # CompanySummary 객체가 이미 정의되어 있다고 가정
        return json.dumps({
            "title": company_summary.title,
            "move": [
                {
                    "field": detail.field,
                    "current_activity": detail.current_activity
                } for detail in company_summary.move
            ],
            "summary": company_summary.summary
        }, indent=4 , ensure_ascii= False)
    except Exception as e:
        print(f"Error converting CompanySummary to JSON: {str(e)}")
        return None

