from datetime import datetime

from airflow.operators.empty import EmptyOperator

from airflow import DAG

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
    start = EmptyOperator(task_id="start")

    end = EmptyOperator(task_id="end")

    start >> end
