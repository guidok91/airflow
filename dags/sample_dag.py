from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

dag = DAG(
    'sample',
    description='Sample DAG',
    start_date=datetime(2018, 1, 1)
)

start = DummyOperator(
    task_id='start',
    dag=dag
)


end = DummyOperator(
    task_id='end',
    dag=dag
)

start >> end
