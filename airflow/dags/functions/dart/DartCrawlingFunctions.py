import time

import dart_fss as dart
import gridfs
import yaml
from dart_fss.corp import Corp
from dart_fss.errors import NoDataReceived
from dart_fss.filings.reports import Report
from dart_fss.filings.search_result import SearchResults
from pymongo import MongoClient
from hdfs import InsecureClient

_appendable_set: set = {"사업의 내용", "사업의 개요", "주요 제품 및 서비스", "매출 및 수주상황",
                        "주요계약 및 연구개발활동", "기타 참고사항", "연구개발실적"}

default_chunk_size: int = 1048576

with open("/usr/local/airflow/config.yaml", 'r') as configuration:
    property_data = yaml.load(configuration, Loader=yaml.FullLoader)
    dart.set_api_key(property_data["crawler"]["dart_secret"])


class NoSuchElementError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def delete_all_data() -> None:
    client = MongoClient("mongodb://admin:ssafya606@j11a606.p.ssafy.io:27017")
    database = client['company_db']

    bucket = gridfs.GridFSBucket(database)

    for element in bucket.find({}):
        bucket.delete(element._id)


def search_corp() -> None:
    """
    키워드와 Dart API를 활용하여 해당 기업의 사업보고소 및 분기 보고서를 받는 함수
    :return:
    """
    corp_data = dart.get_corp_list()
    with open("/usr/local/airflow/include/data.txt", 'r') as file:
        while True:
            corp_name: str = file.readline().replace("\n", "")

            if not corp_name:
                break

            result_data: list = corp_data.find_by_corp_name(corp_name=corp_name)

            if not result_data:
                continue

            for target in result_data:
                target_info: dict = target.to_dict()

                if target_info["corp_name"] == corp_name:
                    _get_business_report(target)

            time.sleep(20)


def _get_business_report(corp: Corp) -> None:
    try:
        reports: SearchResults = corp.search_filings(bgn_de="20221231", end_de="20241001", pblntf_detail_ty="a001")
        _get_data(reports)
    except NoDataReceived:
        return


def _get_data(reports: SearchResults) -> None:
    reports_meta_dict: dict = reports.to_dict()

    idx = 0
    for report in reports:
        corp_name: str = reports_meta_dict["report_list"][idx]["corp_name"]
        report_name: str = reports_meta_dict["report_list"][idx]["report_nm"]
        _make_html_file(report, corp_name, report_name)
        idx += 1


def _make_html_file(report: Report, corp_name: str, report_name: str) -> None:
    client = MongoClient("mongodb://admin:ssafya606@j11a606.p.ssafy.io:27017")
    database = client['company_db']

    bucket = gridfs.GridFSBucket(database)

    #하둡
    hadoop_client = InsecureClient('http://j11a606a.p.ssafy.io:9870', user='hadoop')
    hdfs_file_path = f'/data/dart/{company_name}/{report_name}/{company_name}.json'

    for page in report.pages:
        page_dict: dict = page.to_dict()
        # 디버깅해야함
        for element in _appendable_set:

            if element in page_dict['title']:
                filename: str = corp_name + " " + report_name + " " + page_dict['title']
                metadata: dict = {
                    "contentType": "text/html",
                    "corp_name": corp_name
                }

                with bucket.open_upload_stream(filename=filename, chunk_size_bytes=default_chunk_size,
                                               metadata=metadata) as gridIn:
                    gridIn.write(page.html.encode("utf-8"))
                
                # 하둡 저장
                hadoop_client.write(hdfs_file_path, data=page.html.encode("utf-8"))


if __name__ == "__main__":
    delete_all_data()
    client = MongoClient("mongodb://admin:ssafya606@j11a606.p.ssafy.io:27017")
    database = client['company_db']

    bucket = gridfs.GridFSBucket(database)

    cnt = 0
    for data in bucket.find({"metadata.corp_name": "삼성전자"}):
        # with open(f"./result_{cnt}.html", "w", encoding="utf-8") as file:
        #     file.write(data.read().decode("utf-8"))
        bucket.delete(data._id)

        cnt += 1

    print(cnt)

    # with open("/usr/local/airflow/config.yaml", 'r') as configuration:
    #     property_data = yaml.load(configuration, Loader=yaml.FullLoader)
    #     dart.set_api_key(property_data["crawler"]["dart_secret"])
    #
    # result_data = dart.get_corp_list()
    # dataset = []
    #
    # with open("/usr/local/airflow/include/data.txt", 'r') as file:
    #     while True:
    #         corp_name: str = file.readline()
    #
    #         if not corp_name:
    #             break
    #
    #         dataset.append(corp_name.replace("\n", ""))
    #
    # print(dataset[:10])
    #
    # for element in dataset[:10]:
    #     res = result_data.find_by_corp_name(corp_name=element, exactly=True)
    #     print(res)
    #
    # print(result_data.find_by_corp_name(corp_name="LG디스플레이"))
