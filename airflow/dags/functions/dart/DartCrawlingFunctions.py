import os

import dart_fss as dart
import yaml
from dart_fss.corp import Corp
from dart_fss.filings.reports import Report
from dart_fss.filings.search_result import SearchResults

_appendable_set: set = {"사업의 내용", "사업의 개요", "주요 제품 및 서비스", "매출 및 수주상황",
                        "주요계약 및 연구개발활동", "기타 참고사항", "연구개발실적"}

with open("/usr/local/airflow/config.yaml", 'r') as configuration:
    property_data = yaml.load(configuration, Loader=yaml.FullLoader)
    dart.set_api_key(property_data["crawler"]["dart_secret"])


class NoSuchElementError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def search_corp() -> None:
    """
    키워드와 Dart API를 활용하여 해당 기업의 사업보고소 및 분기 보고서를 받는 함수
    :return:
    """
    result_data: list = dart.get_corp_list().find_by_corp_name("삼성전자")

    is_exists: bool = False
    for target in result_data:
        target_info: dict = target.to_dict()

        if target_info["corp_name"] == "삼성전자":
            _get_business_report(target)
            is_exists = True

    if not is_exists:
        raise NoSuchElementError("키워드에 해당하는 데이터가 없습니다.")


def _get_business_report(corp: Corp) -> None:
    reports: SearchResults = corp.search_filings(bgn_de="20230101", end_de="20240901", pblntf_detail_ty="a001")
    _get_data(reports)


def _get_data(reports: SearchResults) -> None:
    reports_meta_dict: dict = reports.to_dict()
    corp_name: str = reports_meta_dict["report_list"][0]["corp_name"]
    report_name: str = reports_meta_dict["report_list"][0]["report_nm"]

    for report in reports:
        _make_html_file(report, corp_name, report_name)


def _make_html_file(report: Report, corp_name: str, report_name: str) -> None:
    os.makedirs("/usr/local/airflow/temp", exist_ok=True)

    for page in report.pages:
        page_dict: dict = page.to_dict()
        # 디버깅해야함
        for element in _appendable_set:
            print(page_dict['title'] + " " + element)
            if element in page_dict['title']:
                with open(
                        "/usr/local/airflow/temp/" + corp_name + " " + report_name + " " + page_dict['title'] + ".html",
                        'w') as html_file:
                    html_file.write(page.html)

# if __name__ == '__main__':
#     init()
#
#     corp: Corp = search_corp()
#     results: SearchResults = get_business_report(corp)
#
#     get_data(results)
