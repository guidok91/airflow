init:
	pip install --upgrade pip setuptools && pip install -r requirements.txt

init_airflow:
	airflow initdb
	airflow version

run:
	make web
	make schedule

web:
	airflow webserver -D

schedule:
	airflow scheduler
