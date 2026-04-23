from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from scrape import get_data
from insert_data import insert_to_db


def scrape_task(ti):
    data = get_data()
    ti.xcom_push(key="scraped_data", value=data)


def insert_task(ti):
    data = ti.xcom_pull(task_ids='scrape', key='scraped_data')
    insert_to_db(data)


with DAG(
    dag_id="wired_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    scrape = PythonOperator(
        task_id="scrape",
        python_callable=scrape_task
    )

    insert = PythonOperator(
        task_id="insert",
        python_callable=insert_task
    )

    scrape >> insert