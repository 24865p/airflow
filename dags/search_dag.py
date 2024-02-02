import json

from lib.crawling import naver_search
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

config_file = "config.json"

with open(config_file, "r") as file:
    config = json.load(file)


def collect_queries(**kwargs):
    query_list = config.get("query_list")
    search_list = config.get("search_list")
    client_id = config.get("client_id")
    client_secret = config.get("client_secret")

    for query in query_list:
        for search in range(len(search_list)):
            output_file = f"{search_list[search]}.json"
            naver_search(
                search_list[search], query, client_id, client_secret, output_file
            )


dag = DAG(
    "search_dag",
    default_args=default_args,
    description=config.get("description"),
    schedule_interval=timedelta(days=config.get("schedule")),
)

data_task = PythonOperator(
    task_id="collect_data", python_callable=collect_queries, dag=dag
)

data_task
