# services/airflow/dags/hello_world.py
from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator


with DAG(dag_id="hello_world",
  start_date=datetime(2022, 1, 1),
  schedule="* * * * *") as dag:
  # Tasks are represented as operators
  # Use Bash operator to create a Bash task
    hello = BashOperator(task_id="hello", bash_command="echo hello")
    # Python task
    @task()
    def world():
        print("world")

    hello >> world()