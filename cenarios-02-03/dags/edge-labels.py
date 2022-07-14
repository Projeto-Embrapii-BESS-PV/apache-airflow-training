from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.edgemodifier import Label
from datetime import timedelta, datetime 

def check_acuracy(ti):
    acuracy_value = int(ti.xcom_pull(key="model_acuracy"))
    if acuracy_value >= 90:
        return 'deploy_task'
    else:
        return 'retrain_task'

with DAG(
    'edge_labels',
    description='DAG com edge labels e branching',
    schedule_interval=timedelta(minutes=10),
    start_date=datetime.today(),
    is_paused_upon_creation=False # inicia (unpause) a DAG assim que ela subir pro airflow pois ela é iniciada como paused
) as dag:

    push_acuracy_op = BashOperator(
        task_id='push_acuracy_task',
        bash_command='echo "{{ ti.xcom_push(key="model_acuracy", value=90) }}"'
    )

    check_acuracy_op = BranchPythonOperator(
        task_id='check_acuracy_task',
        python_callable=check_acuracy
    )

    deploy_op = DummyOperator(task_id='deploy_task')
    retrain_op = DummyOperator(task_id='retrain_task')
    notify_op = DummyOperator(task_id='notify_task', trigger_rule=TriggerRule.NONE_FAILED)

    push_acuracy_op >> check_acuracy_op
    check_acuracy_op >> Label("ACC >= 90%") >> deploy_op >> notify_op
    check_acuracy_op >> Label("ACC < 90%") >> retrain_op >> notify_op