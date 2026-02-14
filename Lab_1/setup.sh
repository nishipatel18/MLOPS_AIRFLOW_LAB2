#!/bin/bash
set -e

echo "=== Lab 1 Setup: Wine Quality Classification ==="

mkdir -p dags/src dags/data config working_data logs plugins

echo "AIRFLOW_UID=$(id -u)" > .env
echo "Created .env with AIRFLOW_UID=$(id -u)"

echo ""
echo "Checking Docker memory..."
docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'

if [ ! -f docker-compose.yaml ]; then
    echo "Fetching docker-compose.yaml..."
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.1/docker-compose.yaml'
fi

echo ""
echo "=== Lab 1 Setup Complete ==="
echo "Next: docker compose up airflow-init && docker compose up"
