# Airflow Lab Instructions and Description

## Introduction
This document provides a detailed breakdown of the two DAGs (Airflow_Lab2 and Airflow_Lab2_Flask) for the Wine Quality Classification pipeline.

## Prerequisites
- Basic understanding of Apache Airflow concepts
- Apache Airflow installed and configured
- Necessary Python packages installed, including Flask

## Airflow Email Configuration

### Sign in with app passwords
Follow the instruction provided here: [link](https://support.google.com/accounts/answer/185833) and get your smtp password

### Adding SMTP Information to airflow.cfg
```
smtp_host = smtp.gmail.com
smtp_starttls = True
smtp_ssl = False
smtp_user = YOUREMAIL@gmail.com
smtp_password = Enter your password generated above
smtp_port = 587
smtp_mail_from = YOUREMAIL@gmail.com
smtp_timeout = 30
smtp_retry_limit = 5
```

## DAG Structure

### Airflow_Lab2
This DAG orchestrates a Wine Quality Random Forest classification pipeline:
- **owner_task** BashOperator: Echoes 1, demonstration task
- **load_data_task**: Loads wine_quality.csv
- **data_preprocessing_task**: Scales features, train/test split
- **separate_data_outputs_task**: Passthrough task
- **build_save_model_task**: Trains Random Forest, saves model
- **load_model_task**: Loads model, prints score
- **trigger_dag_task**: Triggers Airflow_Lab2_Flask DAG

### Airflow_Lab2_Flask
This DAG manages the Flask API lifecycle:
- **get_latest_run_info()**: Queries Airflow API for last DAG run status
- **Flask Routes**: `/`, `/success`, `/failure`, `/health`
- **start_flask_app()**: Starts Flask server on port 5555
