from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 9, 27),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="etl_clientes",
    default_args=default_args,
    schedule="40 * * * *",
    catchup=False,
    max_active_runs=1,
    render_template_as_native_obj=True,
    tags=["debug", "serialization"],
) as dag:

    @task
    def extract():
        print("Extracting data...")

    @task
    def transform():
        print("Transforming data...")

    @task
    def load():
        print("Loading data...")

    extract() >> transform() >> load()
