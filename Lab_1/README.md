# Airflow Lab 1 — Wine Quality Classification Pipeline

In order to install Airflow using docker you can watch our Airflow Lab1 Tutorial Video

## ML Model
This script is designed for wine quality classification using Random Forest and determining the optimal number of estimators using accuracy convergence. It provides functionality to load data from a CSV file, perform data preprocessing, build and save a Random Forest model, and determine the best n_estimators.

### Prerequisites
Before using this script, make sure you have the following libraries installed:

- pandas
- scikit-learn (sklearn)
- pickle
- base64

### Usage
You can use this script to perform Random Forest classification on the Wine Quality dataset as follows:

```python
# Load the data
data = load_data()

# Preprocess the data
preprocessed_data = data_preprocessing(data)

# Build and save the classification model
accuracy_scores = build_save_model(preprocessed_data, 'model.sav')

# Load the saved model and determine optimal n_estimators
result = load_model_elbow('model.sav', accuracy_scores)
print(result)
```

### Functions

**load_data():**
- Description: Loads Wine Quality data from a CSV file, serializes it, and returns the serialized data.

**data_preprocessing(data):**
- Description: Deserializes data, performs data preprocessing (scaling with MinMaxScaler), and returns serialized processed data.

**build_save_model(data, filename):**
- Description: Builds a Random Forest model with different n_estimators, saves the best model, and returns accuracy scores.

**load_model_elbow(filename, accuracy_scores):**
- Description: Loads a saved Random Forest model and determines the optimal n_estimators using accuracy convergence.

## Airflow Setup

### Prerequisites
You should allocate at least 4GB memory for the Docker Engine (ideally 8GB).

### Tutorial

1. Create a new directory
```bash
mkdir -p ~/app
cd ~/app
```

2. Fetch docker-compose.yaml
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.1/docker-compose.yaml'
```

3. Setting the right Airflow user
```bash
mkdir -p ./dags ./logs ./plugins ./working_data
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

4. Update the following in docker-compose.yml
```yaml
AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
_PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:- pandas scikit-learn }
- ${AIRFLOW_PROJ_DIR:-.}/working_data:/opt/airflow/working_data
_AIRFLOW_WWW_USER_USERNAME: ${_AIRFLOW_WWW_USER_USERNAME:-airflow2}
_AIRFLOW_WWW_USER_PASSWORD: ${_AIRFLOW_WWW_USER_PASSWORD:-airflow2}
```

5. Initialize the database
```bash
docker compose up airflow-init
```

6. Running Airflow
```bash
docker compose up
```

7. Visit localhost:8080 login with credentials set on step 4

8. Find `Airflow_Lab1` DAG, toggle ON, and trigger it

### Stop docker containers
```bash
docker compose down
```
