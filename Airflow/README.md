# Description

The aim of this part is to simulate work flow from GCP to AWS. Data comes from bigquery. I used [workflow](https://github.com/BGD23-xin/ETL_Gcp_Kafka_Airflow_AWS/blob/operation/Airflow/dags/workflow_1.py) to simulate the production of data and store them on Kafka.

The another [workflow](https://github.com/BGD23-xin/ETL_Gcp_Kafka_Airflow_AWS/blob/operation/Airflow/dags/workflow_2.py) is uesd to simulate to consumer data from kafka and finally store them on Athena