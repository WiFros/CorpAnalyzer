import requests
import yaml
from requests import Response


class CrawlingException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


_URL: str = 'https://openapi.naver.com/v1/search/news.json'
_NAVER_NEWS_PREFIX: str = 'n.news.naver.com'
_FILE_PATH_PREFIX: str = "/usr/local/airflow/include/group"


def init_data() -> dict:
    property_data: dict = {}

    with open("/usr/local/airflow/config.yaml", 'r') as configuration:
        props = yaml.load(configuration, Loader=yaml.FullLoader)

        property_data["api_client"] = props["crawler"]["api_client"]
        property_data["api_secret"] = props["crawler"]["api_secret"]
        property_data["display"] = props["crawler"]["crawler_display"]
        property_data["sort"] = props["crawler"]["crawler_sort"]

    return property_data


def read_file(file_number: int) -> list[str]:
    company_name_list: list[str] = []

    with open(_FILE_PATH_PREFIX + str(file_number) + ".txt", 'r') as company_group_file:
        while True:
            line: str = company_group_file.readline()
            if not line:
                break
            company_name_list.append(line.strip())

    return company_name_list


def crawl_news(file_number: int, **context) -> list[list[dict]]:
    property_data: dict = context['task_instance'].xcom_pull(task_ids='init_data')
    company_name_list: list[str] = context['task_instance'].xcom_pull(task_ids=f'read_file_{file_number}')

    _header_property: dict = {
        "X-Naver-Client-Id": property_data["api_client"],
        "X-Naver-Client-Secret": property_data["api_secret"],
    }

    result_list = []

    for corp in company_name_list:
        for i in range(1, 1000, 100):
            tmp_payload: dict = {
                "query": corp,
                "display": property_data["display"],
                "start": i,
                "sort": property_data["sort"],
            }

            response: Response = requests.get(_URL, headers=_header_property, params=tmp_payload)

            if 200 <= response.status_code < 300:
                data: dict = response.json()
                articles: list[dict] = data['items']

                result_list.append(articles)

    return result_list


def filtering_news(file_number: int, **context) -> list[dict]:
    article_list: list[list[dict]] = context['task_instance'].xcom_pull(task_ids=f'crawl_news_{file_number}')
    filtered_articles: list = []

    for row in article_list:
        for article in row:
            article_link: str = article['link']

            if _NAVER_NEWS_PREFIX in article_link:
                title: str = article['title']
                published_at: str = article['pubDate']
                element: dict = {
                    "title": title,
                    "link": article_link,
                    "pubDate": published_at
                }
                filtered_articles.append(element)

    return filtered_articles
