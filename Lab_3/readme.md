A comprehensive guide to setting up, deploying, and triggering Apache Airflow DAGs on a virtual machine (VM). This walkthrough covers creating an Airflow environment, configuring the API, structuring folders, and setting up DAGs to run a Wine Quality Random Forest classification script with email notifications.

## Step-by-Step Guide: Deploying and Triggering Airflow DAGs on a VM

### 1. Create and Configure a VM
1. Create a Virtual Machine Instance:
   - Log in to your cloud provider and create a new VM instance with sufficient resources (e.g., 2 vCPUs, 4GB RAM).
2. Set Up Networking:
   - Add a firewall rule to allow HTTP (port 80) and Airflow webserver port (port 8080).

### 2. Update and Install Necessary Packages
```bash
sudo apt update
sudo apt install python3-pip python3-venv python3-full -y
```

### 3. Set Up a Virtual Environment for Airflow
```bash
python3 -m venv airflow_new_venv
source airflow_new_venv/bin/activate
pip install apache-airflow
airflow db init
```

### 4. Start the Airflow Webserver and Scheduler
Terminal 1:
```bash
source airflow_new_venv/bin/activate
airflow webserver --port 8080
```

Terminal 2:
```bash
source airflow_new_venv/bin/activate
airflow scheduler
```

### 5. Enable the Airflow API
```bash
nano ~/airflow/airflow.cfg
```
```ini
[api]
auth_backend = airflow.api.auth.backend.basic_auth
```

### 6. Create an Airflow Admin User
```bash
airflow users create \
  --username yourusername \
  --firstname yourname \
  --lastname yourname \
  --role Admin \
  --email youremail
```

### 7. Set Up Folder Structure
```bash
mkdir dags
mkdir dags/src
touch requirements.txt
```

Structure:
```
airflow/
├── dags/
│   ├── my_dag.py
│   └── src/
│       ├── model_development.py
│       └── success_email.py
└── requirements.txt
```

### 8. Install Requirements
```bash
pip install -r requirements.txt
```

### 9. Trigger the DAG
```bash
source airflow_new_venv/bin/activate
airflow dags trigger sample_dag
```

### 10. Test Locally
```bash
python3 dags/my_dag.py
```

## Recap of Key Commands
```bash
python3 -m venv airflow_new_venv
source airflow_new_venv/bin/activate
airflow db init
airflow webserver --port 8080
airflow scheduler
airflow dags trigger sample_dag
```
