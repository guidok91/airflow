import os
from datetime import datetime, timedelta

from airflow.operators.empty import EmptyOperator
from astronomer.providers.apache.livy.operators.livy import LivyOperatorAsync

from airflow import DAG

DAG_DEFAULT_ARGS = {
    "owner": "Guido Kosloff Gancedo",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
LIVY_PROXY_USER = "datalake-srv-user"
LIVY_CONN_ID = "livy_emr_conn"
ETL_CODE_LOCATION = "s3://movies-binaries/movies-etl/latest"
SPARK_CONF = {
    "master": "yarn",
    "deploy-mode": "cluster",
    "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
    "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    "spark.yarn.appMasterEnv.ENV_FOR_DYNACONF": os.environ["ENVIRONMENT"],
}
SPARK_JARS = ["io.delta:delta-core_2.12:2.2.0"]


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
        args=[
            "--task",
            "standardize",
            "--execution-date",
            "{{ ds }}",
            "--config-file-path",
            "app_config.yaml",
        ],
        conf=SPARK_CONF,
        py_files=[f"{ETL_CODE_LOCATION}/libs.zip"],
        files=[f"{ETL_CODE_LOCATION}/app_config.yaml"],
        jars=SPARK_JARS,
    )

    curate = LivyOperatorAsync(
        task_id="curate",
        proxy_user=LIVY_PROXY_USER,
        livy_conn_id=LIVY_CONN_ID,
        file=f"{ETL_CODE_LOCATION}/main.py",
        args=[
            "--task",
            "curate",
            "--execution-date",
            "{{ ds }}",
            "--config-file-path",
            "app_config.yaml",
        ],
        conf=SPARK_CONF,
        py_files=[f"{ETL_CODE_LOCATION}/libs.zip"],
        files=[f"{ETL_CODE_LOCATION}/app_config.yaml"],
        jars=SPARK_JARS,
    )

    (
        EmptyOperator(task_id="start")
        >> standardize
        >> curate
        >> EmptyOperator(task_id="end")
    )
