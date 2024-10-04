# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.utils.dates import days_ago
# from pathlib import Path
# import subprocess
#
# # Define paths
# RAW_DATA_PATH = "data/raw/CO2_emission.csv"
# PREPROCESS_SCRIPT = "code/datasets/preprocess_data.py"
# OUTPUT_TRAIN_DATA = "data/preprocessed/train_data.csv"
# OUTPUT_TEST_DATA = "data/preprocessed/test_data.csv"
#
# # Define preprocessing function
# def preprocess_data():
#     """Run the preprocessing script."""
#     subprocess.run(["python3", PREPROCESS_SCRIPT], check=True)
#
# # Define a check for file existence
# def check_file_exists(file_path):
#     if not Path(file_path).is_file():
#         raise FileNotFoundError(f"{file_path} does not exist.")
#
# # Define DAG
# with DAG(
#     'data_pipeline',
#     default_args={'owner': 'airflow'},
#     description='Data pipeline with preprocessing',
#     schedule_interval=None,  # Run manually or define your schedule
#     start_date=days_ago(1),  # You can adjust this as needed
#     catchup=False,
# ) as dag:
#
#     # Check if raw data exists
#     check_raw_data = PythonOperator(
#         task_id="check_raw_data",
#         python_callable=check_file_exists,
#         op_args=[RAW_DATA_PATH]
#     )
#
#     # Preprocess the data
#     preprocess_task = PythonOperator(
#         task_id="preprocess_data",
#         python_callable=preprocess_data,
#     )
#
#     # Check if train and test data outputs exist
#     check_train_output = PythonOperator(
#         task_id="check_train_data",
#         python_callable=check_file_exists,
#         op_args=[OUTPUT_TRAIN_DATA]
#     )
#
#     check_test_output = PythonOperator(
#         task_id="check_test_data",
#         python_callable=check_file_exists,
#         op_args=[OUTPUT_TEST_DATA]
#     )
#
#     # Task dependencies
#     check_raw_data >> preprocess_task >> [check_train_output, check_test_output]



from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.bash import BashOperator

from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
dag = DAG(
    'tutorial',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag,
)
dag.doc_md = __doc__

t1.doc_md = """\
#### Task Documentation
You can document your task using the attributes `doc_md` (markdown),
`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
rendered in the UI's Task Instance Details page.
![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
"""
templated_command = """
{% for i in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds, 7)}}"
    echo "{{ params.my_param }}"
{% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    depends_on_past=False,
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag,
)

