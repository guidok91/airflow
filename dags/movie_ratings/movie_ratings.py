from datetime import datetime, timedelta

from airflow import DAG
from astronomer.providers.apache.livy.operators.livy import LivyOperatorAsync

ETL_CODE_LOCATION = "s3://movies-binaries/movies-etl/latest"
LIVY_PROXY_USER = "datalake-srv-user"
LIVY_CONN_ID = "livy-emr-conn"
DAG_DEFAULT_ARGS = {
    "owner": "Guido Kosloff Gancedo",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="movies-etl",
    default_args=DAG_DEFAULT_ARGS,
    start_date=datetime(2021, 1, 1, 0, 0),
    schedule_interval="0 0 * * *",
) as dag:

    standardize = LivyOperatorAsync(
        task_id="standardize",
        proxy_user=LIVY_PROXY_USER,
        livy_conn_id=LIVY_CONN_ID,
        file=f"{ETL_CODE_LOCATION}/main.py",
        args=["--task", "standardize", "--execution-date", "{{ ds }}"],
        conf={"master": "yarn", "deploy-mode": "cluster"},
        py_files=[f"{ETL_CODE_LOCATION}/libs.zip"],
    )

    curate = LivyOperatorAsync(
        task_id="curate",
        proxy_user=LIVY_PROXY_USER,
        livy_conn_id=LIVY_CONN_ID,
        file=f"{ETL_CODE_LOCATION}/main.py",
        args=["--task", "curate", "--execution-date", "{{ ds }}"],
        conf={"master": "yarn", "deploy-mode": "cluster"},
        py_files=[f"{ETL_CODE_LOCATION}/libs.zip"],
    )

    standardize >> curate
