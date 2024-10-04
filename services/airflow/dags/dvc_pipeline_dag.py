# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from datetime import datetime, timedelta
#
# # Define default arguments for the DAG
# default_args = {
#     'owner': 'airflow',
#     'start_date': datetime(2024, 10, 4),
#     'retries': 1,
#     'retry_delay': timedelta(minutes=1),
# }
#
# # Create the DAG instance
# with DAG('dvc_pipeline_dag', default_args=default_args, schedule_interval='*/5 * * * *', catchup=False) as dag:
#     # Define the DVC pipeline task
#     run_dvc_pipeline = BashOperator(
#         task_id='run_dvc_pipeline',
#         bash_command='dvc repro',  # Command to run the DVC pipeline
#     )
#
#     run_dvc_pipeline
#
# # Note: Don't forget to place this file in the correct DAGs folder for Airflow to recognize it.



from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta, datetime

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 4),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'dvc_pipeline',
    default_args=default_args,
    description='A DVC pipeline for data processing, training, evaluation, and launching containers',
    schedule_interval=timedelta(minutes=5),  # Run every 5 minutes
)

# Define the stages using BashOperator
clean_task = BashOperator(
    task_id='clean_data',
    bash_command='dvc run -n clean -d data/raw/CO2_emission.csv -d code/datasets/preprocess_data.py '
                 '-o data/preprocessed/train_data.csv -o data/preprocessed/test_data.csv '
                 'python3 code/datasets/preprocess_data.py',
    dag=dag,
)

train_model_task = BashOperator(
    task_id='train_model',
    bash_command='dvc run -n train_model -d data/preprocessed/train_data.csv -d code/models/train_model.py '
                 '-o models/model.pkl '
                 'python3 code/models/train_model.py',
    dag=dag,
)

# # Define tasks to launch the containers
# launch_fastapi_task = BashOperator(
#     task_id='launch_fastapi',
#     bash_command='docker run -d --name fastapi --restart unless-stopped -p 8000:8000 '
#                  'your_fastapi_image',  # Replace with your FastAPI image name
#     dag=dag,
# )
#
# launch_streamlit_task = BashOperator(
#     task_id='launch_streamlit',
#     bash_command='docker run -d --name streamlit --restart unless-stopped -p 8501:8501 '
#                  '--link fastapi your_streamlit_image',  # Replace with your Streamlit image name
#     dag=dag,
# )

# Set task dependencies
clean_task >> train_model_task #>> launch_fastapi_task >> launch_streamlit_task
