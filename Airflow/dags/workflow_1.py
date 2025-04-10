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
    "workflow_1",
    default_args=default_args,
    description="A simple test DAG",
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    install_packages = BashOperator(
        task_id="install_packages",
        bash_command="pip install -r /opt/airflow/dags/requirements.txt",
    )

    import_data_to_kafka = BashOperator(
        task_id="import_data_to_Kafka",
        bash_command='python /opt/airflow/dags/producer_data_final.py "2019-03-01"',
    )

    install_packages >> import_data_to_kafka
