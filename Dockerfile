# Start from the official Airflow image
FROM apache/airflow:2.9.0

# Copy requirements and install extra packages
COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

# Copy config script into the image (bot_producer_llm.py is mounted via docker-compose.yaml)
COPY bot_app/config.py /opt/airflow/config.py

# Set the working directory
WORKDIR /opt/airflow