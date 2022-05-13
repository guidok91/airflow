from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime

with DAG(
    dag_id="dummy",
    default_args={
        "owner": "Guido Kosloff Gancedo",
        "depends_on_past": False,
        "email_on_failure": False,
        "email_on_retry": False,
    },
    start_date=datetime(2021, 1, 1, 0, 0),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    start = DummyOperator(
        task_id="start"
    )

    end = DummyOperator(
        task_id="end"
    )

    start >> end
