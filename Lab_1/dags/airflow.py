from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta
from src.model_development import load_data, data_preprocessing, build_model, load_model
from src.success_email import send_success_email

default_args = {
    'owner': 'Nishi Patel',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'sample_dag',
    default_args=default_args,
    description='Wine Quality Random Forest Pipeline for VM Deployment',
    schedule=None,
    catchup=False,
    tags=['wine_quality', 'vm', 'lab3'],
) as dag:

    load_data_task = PythonOperator(
        task_id='load_data_task',
        python_callable=load_data,
    )

    data_preprocessing_task = PythonOperator(
        task_id='data_preprocessing_task',
        python_callable=data_preprocessing,
        op_args=[load_data_task.output],
    )

    build_model_task = PythonOperator(
        task_id='build_model_task',
        python_callable=build_model,
        op_args=[data_preprocessing_task.output, "model.sav"],
    )

    load_model_task = PythonOperator(
        task_id='load_model_task',
        python_callable=load_model,
        op_args=[data_preprocessing_task.output, "model.sav"],
    )

    success_email_task = PythonOperator(
        task_id='send_success_email',
        python_callable=send_success_email,
    )

    load_data_task >> data_preprocessing_task >> build_model_task >> load_model_task >> success_email_task

if __name__ == "__main__":
    dag.test()
