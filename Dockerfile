# Start from the official Airflow image
FROM apache/airflow:2.9.0

# Copy requirements and install extra packages
COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt