from datetime import datetime

from airflow.operators.empty import EmptyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator


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
    schedule="@daily",
    catchup=False,
) as dag:
    start = EmptyOperator(task_id="start")

    middle = KubernetesPodOperator(
        task_id="run_python_script",
        name="python-pod",
        namespace="airflow",
        labels={"app": "airflow"},
        image="python:3.12-slim",
        cmds=["python", "-c"],
        arguments=["print('Hello from Kubernetes Pod!')"],
        in_cluster=True,
    )

    end = EmptyOperator(task_id="end")

    start >> middle >> end
