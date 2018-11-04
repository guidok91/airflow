#! /bin/bash
python wait_for_db.py

make init_airflow
make run
