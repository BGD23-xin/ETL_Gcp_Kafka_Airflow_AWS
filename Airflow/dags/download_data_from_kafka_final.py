import sys
import signal
import time
import json
import os
import csv
from collections import OrderedDict
from typing import Optional
from kafka import KafkaConsumer, TopicPartition
import pandas as pd
import boto3
from tqdm import tqdm


def upload_to_s3(local_file_path, remote_key):
    creds_path = r"/opt/airflow/dags/keys/DE_vm_accessKeys.csv"
    df = pd.read_csv(creds_path)
    access_key = df.loc[0, 'Access key ID']
    secret_key = df.loc[0, 'Secret access key']

    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='eu-west-3'
    )

    bucket_name = s3.list_buckets()['Buckets'][0]['Name']
    remote_key="csv_file/" + remote_key
    s3.upload_file(Filename=local_file_path, Bucket=bucket_name, Key=remote_key)
    print(f"✅ 已上传文件到 S3: s3://{bucket_name}/{remote_key}")


def export_kafka_by_key_full_scan_and_upload(
    topic: str,
    target_key: Optional[str],
    config: dict,
    remote_key: str,
    group_id: Optional[str] = None
):
    bootstrap_servers = config.get("bootstrap_servers")
    username = config.get("username")
    password = config.get("password")

    if group_id is None:
        group_id = f"export-all-{int(time.time())}"

    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_servers,
        security_protocol='SASL_PLAINTEXT',
        sasl_mechanism='PLAIN',
        sasl_plain_username=username,
        sasl_plain_password=password,
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        enable_auto_commit=False
    )

    partitions = consumer.partitions_for_topic(topic)
    if not partitions:
        print("❌ 找不到 topic 或无分区")
        return

    topic_partitions = [TopicPartition(topic, p) for p in partitions]
    consumer.assign(topic_partitions)
    consumer.seek_to_beginning(*topic_partitions)
    end_offsets = consumer.end_offsets(topic_partitions)

    print(f"📦 正在扫描所有分区，查找 key = {target_key!r} 的消息（超时限制：20 秒）...")

    value_rows = []
    field_order = None
    finished_partitions = {tp: False for tp in topic_partitions}

    timeout_seconds = 20
    last_data_time = time.time()

    pbar = tqdm(desc="空闲超时倒计时", total=timeout_seconds, ncols=100, unit="s")

    try:
        while not all(finished_partitions.values()):
            now = time.time()
            if now - last_data_time > timeout_seconds:
                print(f"\n⏱️ 超过 {timeout_seconds} 秒没有读取到任何消息，自动退出。")
                break

            records = consumer.poll(timeout_ms=1000)
            if not records:
                pbar.update(1)
                continue

            any_message_received = False

            for tp, messages in records.items():
                for message in messages:
                    any_message_received = True
                    if target_key is None or message.key == target_key:
                        value = message.value
                        if isinstance(value, dict):
                            value.pop('row_hash', None)
                            if field_order is None:
                                field_order = list(value.keys())
                            value_rows.append(value)

                    if message.offset >= end_offsets[tp] - 1:
                        finished_partitions[tp] = True

            if any_message_received:
                last_data_time = now
                pbar.reset()

    finally:
        consumer.close()
        pbar.close()

    if not value_rows:
        print("⚠️ 没有找到任何符合条件的数据，CSV 未生成。")
        return

    unique_rows = {}
    for row in value_rows:
        tripid = row.get("tripid")
        if tripid not in unique_rows:
            unique_rows[tripid] = row

    value_rows = list(unique_rows.values())

    output_file = f"kafka_json_{target_key}.csv"
    with open(output_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_order)
        writer.writeheader()
        for row in value_rows:
            writer.writerow(row)

    print(f"\n✅ 已生成临时文件：{output_file}")
    upload_to_s3(local_file_path=output_file, remote_key=remote_key)

    os.remove(output_file)
    print(f"🗑️ 已删除本地文件：{output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❗用法: python consume_kafka_by_key.py <key>")
        print("例如: python consume_kafka_by_key.py 2019-01-01")
        sys.exit(1)

    key_arg = sys.argv[1]

    kafka_config = {
        'bootstrap_servers': "34.172.121.220:19092,34.172.121.220:29092,34.172.121.220:39092",
        'username': 'vpn',
        'password': 'BCfoV77N'
    }

    export_kafka_by_key_full_scan_and_upload(
        topic='yellow_tripdata',
        target_key=key_arg,
        config=kafka_config,
        remote_key=f"tripdata_{key_arg}.csv"
    )
