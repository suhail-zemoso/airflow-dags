from airflow.sdk.bases.notifier import BaseNotifier
from airflow import DAG
from airflow.decorators import task
from airflow.models.param import Param
from datetime import datetime, timedelta

class MySlackNotifier(BaseNotifier):
    pass  # Minimal implementation for reproduction

with DAG(
    "tester_dag",
    default_args={
        "on_failure_callback": MySlackNotifier(),
        "owner": "test",
        "start_date": datetime(2023, 9, 27),
        "retries": 2,
        "retry_delay": timedelta(minutes=1),
    },
    schedule="40 * * * *",
    catchup=False,
    max_active_runs=1,
    render_template_as_native_obj=True,
    params={"load_past_data": Param(default=False, type="boolean")},
) as dag:
    @task
    def task1():
        raise Exception("Force failure")  # Ensures the task fails

    @task
    def task2():
        pass
    @task
    def task3():
        pass

    task1() >> task2() >> task3()