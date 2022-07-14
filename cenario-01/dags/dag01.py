from datetime import datetime, timedelta

# https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/dag/index.html#airflow.models.dag.DAG
from airflow import DAG

# https://airflow.apache.org/docs/apache-airflow/stable/operators-and-hooks-ref.html
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def py_hello_world():
    import sys
    try:
        print("hello world from Python {}".format(sys.version))
        return 'OK'
    except:
        return 'error'

with DAG(
    'dag-01',
    description='DAG inicial para demonstração dos operadores Bash e Python',
    schedule_interval=timedelta(minutes=5),
    start_date= datetime.now(),
    is_paused_upon_creation=False # inicia (unpause) a DAG assim que ela subir pro airflow pois ela é iniciada como paused
) as dag:

    task_1 = BashOperator(
        task_id="bash_task",
        bash_command='echo "hello world from bash operator"',
    )
    
    task_2 = PythonOperator(
        task_id="python_task",
        python_callable=py_hello_world
    )

    task_1 >> task_2