from datetime import datetime, timedelta
# https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/dag/index.html#airflow.models.dag.DAG
from airflow import DAG
# https://airflow.apache.org/docs/apache-airflow/stable/operators-and-hooks-ref.html
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

path_raw = '/tmp/raw_data.csv'
path_transf = '/tmp/transf_data.csv'

dburl = 'http://influxdb:8086' 
dbport = 8086
dbtoken= 'tokenteste'
dborg='CEAR'
dbuser = 'admin'
dbpassword = 'admin123'

def extract_data():
    import seaborn
    # dataset: https://github.com/mwaskom/seaborn-data/blob/master/taxis.csv
    df = seaborn.load_dataset(
        name='taxis', 
        parse_dates=['pickup'], 
        usecols=['tip', 'pickup'])
    df.head()
    df.info()
    df.to_csv(path_raw, index=False)

def transform_data():
    import pandas as pd
    df = pd.read_csv(path_raw, parse_dates=['pickup'])
    df.rename(
        columns={
            'pickup':'datetime',
            'tip':'gorjeta_reais'
        },
        inplace=True
    )
    df.sort_values(by='datetime', inplace=True)
    df['gorjeta_dolar'] = df['gorjeta_reais']*5
    df.drop(columns=['gorjeta_reais'], inplace=True)
    df['datetime'] = df['datetime'].apply(lambda x: x.replace(year=datetime.today().year))
    df['datetime'] = df['datetime'].apply(lambda x: x.replace(month=datetime.today().month))
    df['datetime'] = df['datetime'].apply(lambda x: x.replace(day=datetime.today().day))
    df.to_csv(path_transf, index = False)

def load_data_into_db():
    import pandas as pd
    from influxdb_client import InfluxDBClient
    from influxdb_client.client.write_api import SYNCHRONOUS
    df = pd.read_csv(path_transf)
    df.set_index('datetime', inplace=True)
    client = InfluxDBClient(url=dburl, token=dbtoken, org=dborg)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(
        bucket="transformed_data", 
        record=df, 
        data_frame_measurement_name="gorjeta_dolar"
    )

with DAG(
    'dag-02',
    description='DAG ETL',
    schedule_interval=timedelta(minutes=5),
    start_date= datetime.now(),
    is_paused_upon_creation=False # inicia (unpause) a DAG assim que ela subir pro airflow pois ela é iniciada como paused
) as dag:

    extract = PythonOperator(
        task_id="extract-task",
        python_callable=extract_data,
    )

    transform = PythonOperator(
        task_id="transform-task",
        python_callable=transform_data,
    )

    load = PythonOperator(
        task_id="load-task",
        python_callable=load_data_into_db,
    )

    clear = BashOperator(
        task_id="Clear",
        bash_command="dags-scripts/clear.sh"
    )

    extract >> transform >> load >> clear