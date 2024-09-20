from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import datetime

from functions.news import NewsCrawlingFunctions
from functions.news import NewsDescriptionFunctions

with DAG(
        dag_id='NewsPipeline',
        start_date=datetime(2021, 11, 1),
        schedule="@once",
        catchup=False,
) as dag:
    init_data = PythonOperator(
        task_id='init_data',
        python_callable=NewsCrawlingFunctions.init_data,
        dag=dag,
    )

    # task 동적 할당 구현
    parallel_read_file_tasks: list = []
    for group_number in range(1, 6):
        task_info = PythonOperator(
            task_id=f'read_file_{group_number}',
            python_callable=NewsCrawlingFunctions.read_file,
            op_args=[group_number],
            dag=dag,
        )

        parallel_read_file_tasks.append(task_info)

    parallel_crawl_news_tasks: list = []
    for group_number in range(1, 6):
        task_info = PythonOperator(
            task_id=f'crawl_news_{group_number}',
            python_callable=NewsCrawlingFunctions.crawl_news,
            op_args=[group_number],
            dag=dag,
        )

        parallel_crawl_news_tasks.append(task_info)

    parallel_filtering_news_tasks: list = []
    for group_number in range(1, 6):
        task_info = PythonOperator(
            task_id=f'filtering_news_{group_number}',
            python_callable=NewsCrawlingFunctions.filtering_news,
            op_args=[group_number],
            dag=dag,
        )

        parallel_filtering_news_tasks.append(task_info)

    parallel_get_processed_article_tasks: list = []
    for group_number in range(1, 6):
        task_info = PythonOperator(
            task_id=f'get_processed_articles_{group_number}',
            python_callable=NewsDescriptionFunctions.get_processed_article,
            op_args=[group_number],
            dag=dag,
        )

        parallel_get_processed_article_tasks.append(task_info)

    print_result = PythonOperator(
        task_id='print_result',
        python_callable=NewsDescriptionFunctions.print_result,
        dag=dag,
    )

    init_data >> parallel_read_file_tasks[0] >> parallel_crawl_news_tasks[0] >> parallel_filtering_news_tasks[0] >> \
    parallel_get_processed_article_tasks[0] >> print_result

    init_data >> parallel_read_file_tasks[1] >> parallel_crawl_news_tasks[1] >> parallel_filtering_news_tasks[1] >> \
    parallel_get_processed_article_tasks[1] >> print_result

    init_data >> parallel_read_file_tasks[2] >> parallel_crawl_news_tasks[2] >> parallel_filtering_news_tasks[2] >> \
    parallel_get_processed_article_tasks[2] >> print_result

    init_data >> parallel_read_file_tasks[3] >> parallel_crawl_news_tasks[3] >> parallel_filtering_news_tasks[3] >> \
    parallel_get_processed_article_tasks[3] >> print_result

    init_data >> parallel_read_file_tasks[4] >> parallel_crawl_news_tasks[4] >> parallel_filtering_news_tasks[4] >> \
    parallel_get_processed_article_tasks[4] >> print_result
