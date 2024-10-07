from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import datetime

from functions.news import NewsCrawlingFunctions
from functions.news import NewsDescriptionFunctions
from functions.news import NewsPreprocessingFunction
from comm.elastic_search import ElasticSearchFunction
from comm import LLMFunction

default_args: dict = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
}

with (DAG(
        dag_id='NewsPipeline',
        start_date=datetime(2021, 11, 1),
        schedule="@once",
        catchup=False,
) as dag):
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

    collecting_data = PythonOperator(
        task_id='collecting_data',
        python_callable=NewsDescriptionFunctions.collecting_data,
        dag=dag,
    )

    embedding_processing = PythonOperator(
        task_id='embedding_processing',
        python_callable=NewsPreprocessingFunction.embedding_processing,
        dag=dag,
    )

    ner_processing = PythonOperator(
        task_id='ner_processing',
        python_callable=NewsPreprocessingFunction.ner_processing,
        dag=dag,
    )

    summarization_processing = PythonOperator(
        task_id='summarization_processing',
        python_callable=NewsPreprocessingFunction.summarization_processing,
        dag=dag,
    )

    store_to_elastic_search = PythonOperator(
        task_id='store_to_elastic_search',
        python_callable=ElasticSearchFunction.store_to_elastic_search,
        dag=dag,
    )

    store_to_hadoop = PythonOperator(
        task_id='store_to_hadoop',
        python_callable=NewsPreprocessingFunction.store_to_hadoop,
        dag=dag,
    )

    call_RAG = PythonOperator(
        task_id='call_RAG',
        python_callable=LLMFunction.call_RAG_server,
        dag=dag,
    )

    store_to_mongo = PythonOperator(
        task_id='store_to_mongo',
        python_callable=LLMFunction.store_to_mongo,
        dag=dag,
    )

    init_data >> \
    parallel_read_file_tasks[0] >> parallel_crawl_news_tasks[0] >> parallel_filtering_news_tasks[0] >> \
    parallel_get_processed_article_tasks[0] >> collecting_data >> \
    embedding_processing >> ner_processing >> summarization_processing >> [store_to_elastic_search,
                                                                           store_to_hadoop] >> call_RAG >> store_to_mongo

    init_data >> parallel_read_file_tasks[1] >> parallel_crawl_news_tasks[1] >> parallel_filtering_news_tasks[1] >> \
    parallel_get_processed_article_tasks[1] >> collecting_data

    init_data >> parallel_read_file_tasks[2] >> parallel_crawl_news_tasks[2] >> parallel_filtering_news_tasks[2] >> \
    parallel_get_processed_article_tasks[2] >> collecting_data

    init_data >> parallel_read_file_tasks[3] >> parallel_crawl_news_tasks[3] >> parallel_filtering_news_tasks[3] >> \
    parallel_get_processed_article_tasks[3] >> collecting_data

    init_data >> parallel_read_file_tasks[4] >> parallel_crawl_news_tasks[4] >> parallel_filtering_news_tasks[4] >> \
    parallel_get_processed_article_tasks[4] >> collecting_data
