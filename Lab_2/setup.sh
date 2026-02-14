#!/bin/bash
set -e

echo "=== Lab 2 Setup: Wine Quality + Flask API ==="

mkdir -p dags/src dags/data dags/templates config working_data logs plugins

echo "AIRFLOW_UID=$(id -u)" > .env
echo "Created .env"

echo ""
echo "IMPORTANT: Update SMTP settings in config/airflow.cfg"
echo "=== Lab 2 Setup Complete ==="
echo "Next: docker compose up airflow-init && docker compose up"
