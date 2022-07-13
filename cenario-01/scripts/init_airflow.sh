#!/bin/bash

(airflow db init && \
airflow users create --username admin --password abc123 --firstname FirstName --lastname LastName --role Admin --email admin@example.org
); \
airflow webserver & \
airflow scheduler \
