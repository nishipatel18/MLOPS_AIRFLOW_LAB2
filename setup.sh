#!/bin/bash
set -e

echo "============================================"
echo "  Setting up Airflow Wine Quality Labs"
echo "============================================"
echo ""

echo "--- Setting up Lab 1 ---"
cd Lab_1
mkdir -p dags/src dags/data config working_data logs plugins
echo "AIRFLOW_UID=$(id -u)" > .env
echo "Lab 1 ready."
cd ..

echo "--- Setting up Lab 2 ---"
cd Lab_2
mkdir -p dags/src dags/data dags/templates config working_data logs plugins
echo "AIRFLOW_UID=$(id -u)" > .env
echo "Lab 2 ready."
cd ..

echo "--- Setting up Lab 3 ---"
cd Lab_3
mkdir -p dags/src dags/data
echo "Lab 3 ready."
cd ..

echo ""
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  Lab 1: cd Lab_1 && docker compose up airflow-init && docker compose up"
echo "  Lab 2: cd Lab_2 && docker compose up airflow-init && docker compose up"
echo "  Lab 3: Follow readme.md for VM deployment steps"
