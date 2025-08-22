import sys
import os

# Add plugins directory to Python path
plugins_dir = os.path.expanduser("~/airflow/plugins")
if plugins_dir not in sys.path:
    sys.path.append(plugins_dir)

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Import after adding to path
from custom_bundles.git_bundle import UserSpecificGitDagBundle

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
