from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import datetime
from functions.dart import DartCrawlingFunctions

with DAG(
        dag_id='DartPipeline',
        start_date=datetime(2021, 11, 1),
        schedule="@once",
        catchup=False,
) as dag:

    search_corp = PythonOperator(
        task_id='search_corp',
        python_callable=DartCrawlingFunctions.search_corp,
        dag=dag,
    )

    search_corp