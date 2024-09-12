import requests
import yaml
from requests import Response


class CrawlingException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


_URL: str = 'https://openapi.naver.com/v1/search/news.json'
_NAVER_NEWS_PREFIX: str = 'n.news.naver.com'


def init_data() -> dict:
    property_data: dict = {}

    with open("/usr/local/airflow/config.yaml", 'r') as configuration:
        props = yaml.load(configuration, Loader=yaml.FullLoader)

        property_data["api_client"] = props["crawler"]["api_client"]
        property_data["api_secret"] = props["crawler"]["api_secret"]
        property_data["display"] = props["crawler"]["crawler_display"]
        property_data["sort"] = props["crawler"]["crawler_sort"]

    return property_data


def crawl_news(**context):
    property_data: dict = context['task_instance'].xcom_pull(task_ids='init_data')

    _header_property: dict = {
        "X-Naver-Client-Id": property_data["api_client"],
        "X-Naver-Client-Secret": property_data["api_secret"],
    }

    payload: dict = {
        "query": "삼성전자",
        "display": property_data["display"],
        "start": 1,
        "sort": property_data["sort"],
    }

    response: Response = requests.get(_URL, headers=_header_property, params=payload)

    if 200 <= response.status_code < 300:
        data: dict = response.json()
        articles: list = data['items']

        return articles
    else:
        raise CrawlingException(response.json()["errorMessage"])


def filtering_news(**context) -> list:
    article_list: list[dict] = context['task_instance'].xcom_pull(task_ids='crawl_news')
    filtered_articles: list = []

    for article in article_list:
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
