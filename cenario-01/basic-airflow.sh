#!/bin/bash

docker run -d -p 8080:8080 -v "$PWD/dags:/opt/airflow/dags/" \
--entrypoint=/bin/bash \
--name airflow apache/airflow:latest \
-c '(airflow db init && \
    airflow users create --username admin --password admin123 --firstname Jocelio --lastname Vieira --role Admin --email admin@example.org
    ); \
airflow webserver & \
airflow scheduler \

'
