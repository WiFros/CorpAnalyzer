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

    crawl_news = PythonOperator(
        task_id='crawl_news',
        python_callable=NewsCrawlingFunctions.crawl_news,
        dag=dag,
    )

    filtering_news = PythonOperator(
        task_id='filtering_news',
        python_callable=NewsCrawlingFunctions.filtering_news,
        dag=dag,
    )

    get_processed_article = PythonOperator(
        task_id='get_processed_article',
        python_callable=NewsDescriptionFunctions.get_processed_article,
        dag=dag,
    )

    print_result = PythonOperator(
        task_id='print_result',
        python_callable=NewsDescriptionFunctions.print_result,
        dag=dag,
    )

    init_data >> crawl_news >> filtering_news >> get_processed_article >> print_result
