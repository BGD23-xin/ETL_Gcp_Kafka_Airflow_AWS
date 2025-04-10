import boto3
import pandas as pd


creds_path = r"/opt/airflow/dags/keys/DE_vm_accessKeys.csv"
df = pd.read_csv(creds_path)
access_key = df.loc[0, 'Access key ID']
secret_key = df.loc[0, 'Secret access key']



region = 'eu-west-3'
athena_client = boto3.client(
    "athena",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region,
)


output_location = 's3://de-test-vm-2025/sql_file/'



query="""

CREATE EXTERNAL TABLE IF NOT EXISTS tripdata (
  tripid STRING,
  vendorid BIGINT,
  ratecodeid BIGINT,
  pickup_locationid BIGINT,
  dropoff_locationid BIGINT,
  pickup_datetime TIMESTAMP,
  dropoff_datetime TIMESTAMP,
  store_and_fwd_flag STRING,
  passenger_count BIGINT,
  trip_distance DECIMAL(10,2),
  trip_type BIGINT,
  fare_amount DECIMAL(10,2),
  extra DECIMAL(10,2),
  mta_tax DECIMAL(10,2),
  tip_amount DECIMAL(10,2),
  tolls_amount DECIMAL(10,2),
  ehail_fee DECIMAL(10,2),
  improvement_surcharge DECIMAL(10,2),
  total_amount DECIMAL(10,2),
  payment_type BIGINT,
  payment_type_description STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'field.delim' = ',',
  'serialization.format' = ','
)
STORED AS TEXTFILE
LOCATION 's3://de-test-vm-2025/csv_file/'
TBLPROPERTIES ('skip.header.line.count'='1');
"""

response = athena_client.start_query_execution(
    QueryString=query,
    QueryExecutionContext={
        'Database': 'default'
    },
    ResultConfiguration={
        'OutputLocation': output_location
    }
)

execution_id = response['QueryExecutionId']
print("Query submitted, execution ID:", execution_id)
