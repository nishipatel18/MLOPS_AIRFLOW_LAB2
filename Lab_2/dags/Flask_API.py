import os
import base64
import pendulum
import requests
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from flask import Flask, redirect, render_template

WEBSERVER = os.getenv("AIRFLOW_WEBSERVER", "http://airflow-apiserver:8080")
AF_USER = os.getenv("AIRFLOW_USERNAME", "airflow")
AF_PASS = os.getenv("AIRFLOW_PASSWORD", "airflow")
TARGET_DAG_ID = os.getenv("TARGET_DAG_ID", "Airflow_Lab2")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)


def get_latest_run_info():
    url = f"{WEBSERVER}/api/v2/dags/{TARGET_DAG_ID}/dagRuns?order_by=-run_after&limit=1"
    info = {
        "state": "unknown",
        "run_id": "N/A",
        "logical_date": "N/A",
        "start_date": "N/A",
        "end_date": "N/A",
        "note": ""
    }

    auth_bytes = f"{AF_USER}:{AF_PASS}".encode("ascii")
    base64_auth = base64.b64encode(auth_bytes).decode("ascii")
    headers = {"Accept": "application/json", "Authorization": f"Basic {base64_auth}"}

    try:
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            info["note"] = f"API Error {r.status_code}"
            return False, info

        data = r.json()
        runs = data.get("dag_runs", [])

        if not runs:
            info["note"] = "Waiting for DAG run to appear..."
            return False, info

        run = runs[0]
        state = run.get("state", "unknown")
        print(state)

        info.update({
            "state": state,
            "run_id": run.get("dag_run_id", "N/A"),
            "logical_date": run.get("logical_date") or run.get("run_after", "N/A"),
            "start_date": run.get("start_date", "N/A"),
            "end_date": run.get("end_date", "N/A"),
        })

        if state == "queued" or state == "running":
            info["note"] = "Wine Quality pipeline is still in progress..."
            return False, info

        return state == "success", info

    except Exception as e:
        info["note"] = f"Network issue: {str(e)}"
        return False, info


@app.route("/")
def index():
    ok, _ = get_latest_run_info()
    return redirect("/success" if ok else "/failure")


@app.route("/success")
def success():
    _, info = get_latest_run_info()
    return render_template("success.html", **info)


@app.route("/failure")
def failure():
    _, info = get_latest_run_info()
    return render_template("failure.html", **info)


@app.route("/health")
def health():
    return "ok", 200


def start_flask_app():
    print(f"Starting Flask on 0.0.0.0:5555 checking {WEBSERVER}...", flush=True)
    app.run(host="0.0.0.0", port=5555, debug=False, use_reloader=False)


default_args = {
    "start_date": pendulum.datetime(2024, 1, 1, tz="UTC"),
    "retries": 0,
}

dag = DAG(
    dag_id="Airflow_Lab2_Flask",
    default_args=default_args,
    schedule=None,
    catchup=False,
    is_paused_upon_creation=False,
)

PythonOperator(
    task_id="start_Flask_API",
    python_callable=start_flask_app,
    dag=dag,
)
