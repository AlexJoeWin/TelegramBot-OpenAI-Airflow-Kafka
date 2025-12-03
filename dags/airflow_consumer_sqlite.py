import sqlite3
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from kafka import KafkaConsumer

def consume_to_sqlite():
    # Connect to SQLite (creates file if not exists)
    with sqlite3.connect("telegram.db") as conn:
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS kafka_messages(id INTEGER PRIMARY KEY AUTOINCREMENT, value TEXT, topic TEXT)""")

        # Kafka Consumer setup
        consumer = KafkaConsumer(
            'telegram_topic',
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='sqlite-group')

        print("Listening for Kafka messages...")

        messages = consumer.poll(timeout_ms=5000) # Poll for up to 5 second
        for records in messages.values():
            for record in records:
                cursor.execute(
                    "INSERT INTO kafka_messages (value, topic) VALUES (?, ?)",
                    (record.value.decode("utf-8"), record.topic))
        conn.commit()
        print(f"Stored: {record.value.decode("utf-8")}")

# --- Airflow DAG Definition ---
with DAG(
    dag_id="kafka_consumer_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval="*/5 * * * *",  # runs every 5 min
    catchup=False
) as dag:

    kafka_task = PythonOperator(
        task_id="consume_kafka_topic",
        python_callable=consume_to_sqlite
    )