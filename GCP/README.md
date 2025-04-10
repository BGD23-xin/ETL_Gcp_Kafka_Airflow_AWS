# Description

For this part, i'll show the configuration on the gcp:
- 1. Terraform
- 2. Installations(docker,anaconda)
- 3. Kafka

### 1. Terraform

I used [terraform](https://github.com/BGD23-xin/ETL_Gcp_Kafka_Airflow_AWS/tree/operation/GCP/Terraform) to create a VM on gcp cloud.(you could also create by hand).


### 2.Installations(docker,anaconda)

This part is to configure the environment for the the part of Kafka. I used a [sh file](https://github.com/BGD23-xin/ETL_Gcp_Kafka_Airflow_AWS/blob/operation/GCP/installations/installations_gcp.sh) to run all of codes automatically(you could also follow the steps by my [another project](https://github.com/BGD23-xin/DataEngineering_Terraform_Kestra_bigquery_DBT_LookerStudio/blob/main/installations/README.md)).


### 3.Kafka

I used docker to deploy kafka cluster and kafka UI to look the status of cluster. In the [file](https://github.com/BGD23-xin/ETL_Gcp_Kafka_Airflow_AWS/blob/operation/GCP/installations/docker-compose.yml) of docker compose, you need to pay attention to the external ip, which is the external ip of your vm.

For the simulation of security, i used the mode(SASL_PLAINTEXT). there is one mode strict(SSL), i justed realized by the cluster with zookeeper. This mode is very complex, so i did not used the mode in this project. 