from __future__ import annotations
import pendulum
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.task.trigger_rule import TriggerRule

from src.model_development import (
    load_data,
    data_preprocessing,
    separate_data_outputs,
    build_model,
    load_model,
)

default_args = {
    "start_date": pendulum.datetime(2024, 1, 1, tz="UTC"),
    "retries": 0,
}

dag = DAG(
    dag_id="Airflow_Lab2",
    default_args=default_args,
    description="Wine Quality Random Forest Classification - Lab2",
    schedule="@daily",
    catchup=False,
    tags=["wine_quality"],
    owner_links={"Nishi Patel": "https://github.com/nishipatel18/MLOPS_AIRFLOW_LAB2/"},
    max_active_runs=1,
)

owner_task = BashOperator(
    task_id="task_using_linked_owner",
    bash_command="echo 1",
    owner="Nishi Patel",
    dag=dag,
)

load_data_task = PythonOperator(
    task_id="load_data_task",
    python_callable=load_data,
    dag=dag,
)

data_preprocessing_task = PythonOperator(
    task_id="data_preprocessing_task",
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],
    dag=dag,
)

separate_data_outputs_task = PythonOperator(
    task_id="separate_data_outputs_task",
    python_callable=separate_data_outputs,
    op_args=[data_preprocessing_task.output],
    dag=dag,
)

build_save_model_task = PythonOperator(
    task_id="build_save_model_task",
    python_callable=build_model,
    op_args=[separate_data_outputs_task.output, "model.sav"],
    dag=dag,
)

load_model_task = PythonOperator(
    task_id="load_model_task",
    python_callable=load_model,
    op_args=[separate_data_outputs_task.output, "model.sav"],
    dag=dag,
)

trigger_dag_task = TriggerDagRunOperator(
    task_id="my_trigger_task",
    trigger_dag_id="Airflow_Lab2_Flask",
    conf={"message": "Data from upstream DAG"},
    reset_dag_run=False,
    wait_for_completion=False,
    trigger_rule=TriggerRule.ALL_DONE,
    dag=dag,
)

owner_task >> load_data_task >> data_preprocessing_task >> \
    separate_data_outputs_task >> build_save_model_task >> \
    load_model_task >> trigger_dag_task
