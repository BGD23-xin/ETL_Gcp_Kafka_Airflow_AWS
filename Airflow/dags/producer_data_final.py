import os
import sys
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from kafka import KafkaProducer
import json
from tqdm import tqdm

# === 命令行参数处理 ===
if len(sys.argv) != 2:
    print("❌ 用法错误！请提供日期参数：")
    print("   示例：python wenjian.py 2019-01-01")
    sys.exit(1)

input_date = sys.argv[1]  # 获取日期参数
print(f"🔍 正在处理日期: {input_date}")

# === BigQuery 设置 ===
key_path = r"/opt/airflow/dags/keys/my-creds.json"
credentials = service_account.Credentials.from_service_account_file(key_path)

project_id = "terraform-demo-452020"
data_set_id = "dbt_xxu"
table_id = "stg_traitement__yellow_tripdata"

client = bigquery.Client(credentials=credentials, project=project_id)

query = f"""
    SELECT *
    FROM `{project_id}.{data_set_id}.{table_id}`
    WHERE DATE_TRUNC(pickup_datetime, day) = '{input_date}'
    limit 70000
"""

# === 查询并保存临时 CSV ===
df = client.query(query).to_dataframe()
if df.empty:
    print(f"⚠️ 没有找到日期 {input_date} 的数据。程序结束。")
    sys.exit(0)

csv_path = f"temp_yellow_tripdata_{input_date}.csv"
df.to_csv(csv_path, index=False)

# === Kafka 设置 ===
producer = KafkaProducer(
    bootstrap_servers=["34.172.121.220:19092", "34.172.121.220:29092", "34.172.121.220:39092"],
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism="PLAIN",
    sasl_plain_username="vpn",
    sasl_plain_password="BCfoV77N",
    
    # 🚀 关键可靠性参数

    acks='all',
    retries=5,
    retry_backoff_ms=200,
    # enable_idempotence=True,
    
    linger_ms=10,
    batch_size=32768,

    # 序列化

    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8')
)


topic = "yellow_tripdata"

# === 分批读取并发送 Kafka ===
chunk_size = 500
total_rows = len(df)
num_chunks = (total_rows + chunk_size - 1) // chunk_size

print(f"🚀 共 {total_rows} 行数据，将分为 {num_chunks} 批发送到 Kafka。")

for chunk in tqdm(pd.read_csv(csv_path, chunksize=chunk_size), total=num_chunks, desc="Sending to Kafka"):
    for _, row in chunk.iterrows():
        key = input_date
        value = row.to_dict()
        producer.send(topic, key=key, value=value)
    producer.flush()

# === 删除临时文件 ===
os.remove(csv_path)
print("✅ 全部数据已成功发送并删除临时文件。")
