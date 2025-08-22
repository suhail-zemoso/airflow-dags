import os
import sys
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

    # Test 1: Basic environment check with Python environment setup
    t1 = BashOperator(
        task_id="env_check",
        bash_command="""
        # Set up environment
        export AIRFLOW_HOME="/opt/airflow"
        export PYTHONPATH="$AIRFLOW_HOME:$PYTHONPATH"
        
        # Find Python site-packages
        PYTHON_SITE_PACKAGES=$(python3 -c "import site; print(site.getsitepackages()[0])" 2>/dev/null || echo "/usr/local/lib/$(ls /usr/local/lib/ | grep python)/site-packages")
        
        echo "=== Environment Check ==="
        echo "User: $(whoami)"
        echo "Groups: $(groups)"
        echo "Current dir: $(pwd)"
        echo "Airflow Home: $AIRFLOW_HOME"
        echo "Python Path: $PYTHON_SITE_PACKAGES"
        echo "Python Version: $(python3 --version 2>&1 || echo 'Python not found')"
        
        # Check for custom_bundles module
        echo -e "\n=== Custom Bundles Check ==="
        if [ -d "$PYTHON_SITE_PACKAGES/custom_bundles" ]; then
            echo "custom_bundles found in: $PYTHON_SITE_PACKAGES/custom_bundles"
            ls -la "$PYTHON_SITE_PACKAGES/custom_bundles"
        else
            echo "custom_bundles not found in $PYTHON_SITE_PACKAGES/"
            echo "Contents of $PYTHON_SITE_PACKAGES/:"
            ls -la "$PYTHON_SITE_PACKAGES/" | grep -i bundle || echo "No bundle-related packages found"
        fi
        
        # Check Python path
        echo -e "\n=== Python Environment ==="
        echo "Python executable: $(which python3)"
        python3 -c "import sys; print('\n'.join(sys.path))" 2>&1 || echo "Failed to get Python path"
        
        # Check if we can import the required module
        echo -e "\n=== Module Import Test ==="
        python3 -c "
import sys
print(f'Python version: {sys.version}')
try:
    import custom_bundles
    print('SUCCESS: Imported custom_bundles from:', custom_bundles.__file__)
except ImportError as e:
    print(f'ERROR: {e}')
    print('\nCurrent sys.path:')
    for p in sys.path:
        print(f'  {p}')
"
        
        echo "======================="
        """,
        run_as_user="run_as_suhail",
        env={
            'AIRFLOW_HOME': '/opt/airflow',
            'PYTHONPATH': '/opt/airflow',
            'PATH': os.environ.get('PATH', ''),
            'PYTHONIOENCODING': 'utf-8',
            'LC_ALL': 'C.UTF-8',
            'LANG': 'C.UTF-8'
        }
    )
