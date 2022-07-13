#!/bin/bash

pip install influxdb-client[extra] & \
pip install pandas & \
pip install seaborn  & \
(airflow db init && \
airflow users create --username admin --password admin123 --firstname Jocelio --lastname Vieira --role Admin --email admin@example.org
); \
airflow webserver & \
airflow scheduler \
