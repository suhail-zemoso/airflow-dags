from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    "git_bundle_test",
    start_date=datetime(2025, 1, 2),
    schedule=None,
    catchup=False,
) as dag:

    # Test 1: Simple whoami
    t1 = BashOperator(
        task_id="whoami_task",
        bash_command="whoami && echo 'Current directory:' && pwd && echo 'Environment:' && env",
        run_as_user="run_as_suhail",
    )
    
    # Test 2: Check Python availability
    t2 = BashOperator(
        task_id="python_check_task",
        bash_command="which python3 && python3 --version",
        run_as_user="run_as_suhail",
    )
    
    # Test 3: Run as root for comparison
    t3 = BashOperator(
        task_id="root_check_task",
        bash_command="whoami && which python3 && python3 --version",
    )
    
    t1 >> t2 >> t3
