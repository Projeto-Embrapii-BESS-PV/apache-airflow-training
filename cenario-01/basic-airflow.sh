#!/bin/bash

docker run -d -p 8080:8080 -v "$PWD/dags:/opt/airflow/dags/" \
--entrypoint=/bin/bash \
--name airflow apache/airflow:2.1.1-python3.8 \
-c '(airflow db init && \
    airflow users create --username admin --password abc123 --firstname Felipe --lastname Lastname --role Admin --email admin@example.org
    ); \
airflow webserver & \
airflow scheduler \
'
