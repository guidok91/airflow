from datetime import datetime

from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.amazon.aws.operators.emr_add_steps import EmrAddStepsOperator
from airflow.providers.amazon.aws.operators.emr_create_job_flow import EmrCreateJobFlowOperator
from airflow.providers.amazon.aws.operators.emr_terminate_job_flow import EmrTerminateJobFlowOperator
from airflow.providers.amazon.aws.sensors.emr_step import EmrStepSensor

from dags.emr_transient_cluster.settings import EMRClusterConfig, SparkSteps

"""
Sample DAG to run Spark jobs on an EMR transient cluster.
Steps:
    * Spins up an EMR cluster.
    * Waits for it to be ready.
    * Submits Spark jobs to the cluster.
    * Terminates cluster.
"""

with DAG(
    dag_id="emr_transient_cluster",
    default_args={
        "owner": "Guido Kosloff",
        "depends_on_past": False,
        "email_on_failure": False,
        "email_on_retry": False,
    },
    start_date=datetime(2021, 1, 1, 0, 0),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    create_cluster = EmrCreateJobFlowOperator(
        task_id="create_cluster",
        job_flow_overrides=EMRClusterConfig.JOB_FLOW_OVERRIDES,
        aws_conn_id="aws_default",
        emr_conn_id="emr_default",
    )

    add_step_load_raw_data = EmrAddStepsOperator(
        task_id="add_step_load_raw_data",
        job_flow_id=create_cluster.output,
        aws_conn_id="aws_default",
        steps=SparkSteps.LOAD_RAW_DATA,
    )

    wait_for_step_load_raw_data = EmrStepSensor(
        task_id="wait_for_step_load_raw_data",
        job_flow_id=create_cluster.output,
        step_id="{{ task_instance.xcom_pull(task_ids='add_step_load_raw_data', key='return_value')[0] }}",
        aws_conn_id="aws_default",
    )

    add_step_transform = EmrAddStepsOperator(
        task_id="add_step_transform",
        job_flow_id=create_cluster.output,
        aws_conn_id="aws_default",
        steps=SparkSteps.TRANSFORM,
    )

    wait_for_step_transform = EmrStepSensor(
        task_id="wait_for_step_transform",
        job_flow_id=create_cluster.output,
        step_id="{{ task_instance.xcom_pull(task_ids='add_step_transform', key='return_value')[0] }}",
        aws_conn_id="aws_default",
    )

    terminate_cluster = EmrTerminateJobFlowOperator(
        task_id="terminate_cluster",
        job_flow_id=create_cluster.output,
        aws_conn_id="aws_default",
        trigger_rule=TriggerRule.ALL_DONE
    )

    add_step_load_raw_data >> wait_for_step_load_raw_data >> \
        add_step_transform >> wait_for_step_transform >> \
        terminate_cluster
