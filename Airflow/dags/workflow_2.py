from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 13),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "workflow_2",
    default_args=default_args,
    description="A simple test DAG",
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    download_data_from_kafka = BashOperator(
        task_id="download_data_from_Kafka",
        bash_command='python /opt/airflow/dags/download_data_from_kafka_final.py "2019-03-01"',
    )
    
    create_database = BashOperator(
        task_id="create_database",
        bash_command='python /opt/airflow/dags/create_database.py',
    )


    download_data_from_kafka >> create_database