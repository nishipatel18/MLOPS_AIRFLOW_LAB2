# MLOPS_AIRFLOW_LAB2
## Dataset

All three labs use the **UCI Wine Quality (Red Wine)** dataset.

- **Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/wine+quality)
- **Samples:** 1,599 red wine samples
- **Features:** 11 physicochemical properties (fixed acidity, volatile acidity, citric acid, residual sugar, chlorides, free sulfur dioxide, total sulfur dioxide, density, pH, sulphates, alcohol)
- **Target:** Quality score (3–8)

## Model

- **Lab 1:** Random Forest Classifier with accuracy convergence method (similar to elbow method)
- **Lab 2:** Random Forest Classifier with MinMaxScaler + StandardScaler preprocessing
- **Lab 3:** Random Forest Classifier deployed on VM with email notifications

## Labs Overview

| Lab | Focus | Environment | Model |
|-----|-------|-------------|-------|
| Lab 1 | Airflow basics + ML pipeline DAG | Docker | Random Forest (elbow-style tuning) |
| Lab 2 | Email notifications + Flask API + DAG chaining | Docker | Random Forest (Logistic Regression style pipeline) |
| Lab 3 | VM deployment + Airflow API + email notifications | Virtual Machine | Random Forest |

### Lab 1 — Airflow Basics with Docker
- Set up Airflow using Docker Compose
- Build a DAG pipeline: load data → preprocess → train model → evaluate
- Uses XCom with base64 serialization to pass data between tasks
- Determines optimal n_estimators using accuracy convergence

### Lab 2 — Email Notifications + Flask API
- Extends pipeline with BashOperator and TriggerDagRunOperator
- Flask API (`Flask_API.py`) checks DAG run status via Airflow REST API
- HTML templates for success/failure status pages
- Two DAGs: `Airflow_Lab2` (ML pipeline) and `Airflow_Lab2_Flask` (Flask server)

### Lab 3 — VM Deployment
- Deploy Airflow natively on a Virtual Machine (no Docker)
- Configure Airflow API with basic auth
- Success email notification using SMTP
- Trigger DAGs via CLI: `airflow dags trigger sample_dag`

## Folder Structure
```
MLOPS_AIRFLOW_LAB2/
├── Lab_1/
│   ├── config/
│   ├── dags/
│   │   ├── data/          (file.csv, test.csv)
│   │   ├── src/           (__init__.py, lab.py)
│   │   └── airflow.py
│   ├── README.md
│   └── setup.sh
├── Lab_2/
│   ├── config/
│   ├── dags/
│   │   ├── data/          (wine_quality.csv)
│   │   ├── src/           (__init__.py, model_development.py)
│   │   ├── templates/     (success.html, failure.html)
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── Flask_API.py
│   ├── README.md
│   ├── cookies.txt
│   ├── requirements.txt
│   └── setup.sh
├── Lab_3/
│   ├── dags/
│   │   ├── data/          (wine_quality.csv)
│   │   ├── src/           (__init__.py, model_development.py, success_email.py)
│   │   ├── __init__.py
│   │   └── my_dag.py
│   ├── readme.md
│   └── requirements.txt
├── assets/
├── README.md
└── setup.sh
```

## Result Screenshots

### Lab 1
![LAB 1](https://github.com/user-attachments/assets/74a34929-c364-4d85-b12a-f5be3b8d7482)

## Lab 2
![LAB](https://github.com/user-attachments/assets/7893c858-612d-454f-8fa5-96ad028adacf)

## Lab 3
![LAB 3](https://github.com/user-attachments/assets/6809694e-36f5-4237-9402-5fc477a34a5b)

