from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def fetch_and_insert():
    import requests
    import psycopg2

    res = requests.get("http://host.docker.internal:8000/articles")
    data = res.json()["data"]

    conn = psycopg2.connect(
        host="host.docker.internal",
        port=5433,
        database="wired_db",
        user="admin",
        password="admin"
    )

    cur = conn.cursor()

    for item in data:
        cur.execute("""
            INSERT INTO wired_articles (title, url, description, author, scraped_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            item["title"],
            item["url"],
            item["description"],
            item["author"],
            item["scraped_at"]
        ))

    conn.commit()
    cur.close()
    conn.close()


with DAG(
    dag_id="wired_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    task = PythonOperator(
        task_id="fetch_and_insert_data",
        python_callable=fetch_and_insert
    )