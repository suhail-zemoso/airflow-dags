from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    "git_bundle_test",
    start_date=datetime(2025, 1, 2),
    schedule=None,
    catchup=False,
) as dag:

    # Test 1: Run as current user first
    t1 = BashOperator(
        task_id="current_user_check",
        bash_command="echo 'Running as:' && whoami && echo '\nPython path:' && which python3 && echo '\nEnvironment:' && env"
    )
    
    # Test 2: Try to run as run_as_suhail without sudo
    t2 = BashOperator(
        task_id="try_direct_run",
        bash_command="su - run_as_suhail -c 'echo \"Running as: $(whoami)\\nPython path: $(which python3)\\nPython version: $(python3 --version 2>&1)\\n\"' || echo 'Failed to run as run_as_suhail'"
    )
    
    # Test 3: Check if we can create a simple file
    t3 = BashOperator(
        task_id="file_permission_check",
        bash_command="TEST_FILE=/tmp/airflow_test_$(date +%s) && \
                    echo 'Creating test file...' && \
                    touch $TEST_FILE && \
                    echo 'Successfully created file' && \
                    rm $TEST_FILE || \
                    echo 'Failed to create file'"
    )
    
    t1 >> t2 >> t3
