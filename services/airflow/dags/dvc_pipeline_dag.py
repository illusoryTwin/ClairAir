from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 4),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Create the DAG instance
with DAG('dvc_pipeline_dag', default_args=default_args, schedule_interval='*/5 * * * *', catchup=False) as dag:
    # Define the DVC pipeline task
    run_dvc_pipeline = BashOperator(
        task_id='run_dvc_pipeline',
        bash_command='dvc repro',  # Command to run the DVC pipeline
    )

    run_dvc_pipeline

# Note: Don't forget to place this file in the correct DAGs folder for Airflow to recognize it.
