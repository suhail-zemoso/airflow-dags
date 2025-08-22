import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
import json

with DAG(
    "git_bundle_test",
    start_date=datetime(2025, 1, 2),
    schedule=None,
    catchup=False,
) as dag:

    # Test 1: Basic environment check
    t1 = BashOperator(
        task_id="env_check",
        bash_command="""
        echo "=== Environment Check ==="
        echo "User: $(whoami)"
        echo "Groups: $(groups)"
        echo "Current dir: $(pwd)"
        echo "Airflow Home: $AIRFLOW_HOME"
        echo "Python Path: $PYTHONPATH"
        echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
        
        echo -e "\n=== Python Environment ==="
        which python3
        python3 --version
        
        echo -e "\n=== Airflow Config ==="
        if [ -f "$AIRFLOW_HOME/airflow.cfg" ]; then
            echo "airflow.cfg exists"
            ls -la "$AIRFLOW_HOME/airflow.cfg"
            
            # Check if we can read the config
            if [ -r "$AIRFLOW_HOME/airflow.cfg" ]; then
                echo -e "\nairflow.cfg contents (first 20 lines):"
                head -n 20 "$AIRFLOW_HOME/airflow.cfg"
            else
                echo "Cannot read airflow.cfg"
            fi
        else
            echo "airflow.cfg not found in $AIRFLOW_HOME/"
            echo "Contents of $AIRFLOW_HOME/:"
            ls -la "$AIRFLOW_HOME/"
        fi
        
        echo -e "\n=== Directory Permissions ==="
        echo "/opt/airflow permissions:"
        ls -ld /opt/airflow
        echo -e "\n/opt/airflow/shared_dag_bundles permissions:"
        ls -ld /opt/airflow/shared_dag_bundles
        
        echo -e "\n=== Sudo Access ==="
        sudo -n -u run_as_suhail whoami && echo "Sudo access works" || echo "Sudo access failed"
        
        echo "======================="
        """,
        run_as_user="run_as_suhail",
        env={
            'AIRFLOW_HOME': '/opt/airflow',
            'PYTHONPATH': '/opt/airflow',
            'PATH': os.environ.get('PATH', ''),
            'LD_LIBRARY_PATH': os.environ.get('LD_LIBRARY_PATH', '')
        }
    )
