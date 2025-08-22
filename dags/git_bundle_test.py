from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    "git_bundle_test",
    start_date=datetime(2025, 1, 2),
    schedule=None,
    catchup=False,
) as dag:

    t1 = BashOperator(
        task_id="whoami_task",
        bash_command="whoami",
        run_as_user="run_as_suhail",
    )
