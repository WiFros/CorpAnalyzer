import requests
from bs4 import BeautifulSoup
from requests import Response


def get_processed_article(**context) -> list[dict]:
    """
    필터링된 뉴스 dictionary list 에서 링크를 통해 기사의 Full Description 및 Title 을 크롤링해 반환하는 메서드

    :return: 가공된 기사 Title 및 Description dictionary list
    """
    news_info_list: list = context["task_instance"].xcom_pull(task_ids="filtering_news")
    result_list: list = []

    for news_info in news_info_list:
        link: str = news_info['link']
        request_url: str = link.replace('\\', '')

        result_data: dict = _get_description_from_html(_get_html_from_news_info(request_url))
        result_data['pubDate'] = news_info['pubDate']
        result_data['link'] = request_url

        result_list.append(result_data)

    return result_list


def _get_html_from_news_info(request_url: str) -> Response:
    """
    뉴스 링크를 통해 html data를 크롤링하는 메서드

    :param request_url: 타겟 링크
    :return: 링크에서 가져온 html response data
    """

    return requests.get(request_url)


def _get_description_from_html(response: Response) -> dict:
    """
    html response에서 description 및 title을 조회하여 텍스트 데이터만 추출해 반환하는 메서드

    :param response: html response data
    :return: 추출된 텍스트 데이터로 이루어진 dictionary data
    """

    soup = BeautifulSoup(response.text, 'html.parser')
    description: str = soup.select_one('#dic_area').text
    title: str = soup.select_one('#title_area').text

    result_title: str = title.replace('\n', ' ')
    result_description: str = description.replace('\n', ' ')

    return {"title": result_title, "description": result_description}

def print_result(**context) -> None:
    result_list: list[dict] = context["task_instance"].xcom_pull(task_ids="get_processed_article")

    for result_dict in result_list:
        print(result_dict)