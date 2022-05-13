SHELL=/bin/bash

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-rm:
	docker-compose rm -fs

docker-build:
	docker-compose build

setup:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

airflow-start:
	export AIRFLOW__CORE__SQL_ALCHEMY_CONN="postgresql+psycopg2://${POSTGRES_LISTENADDR}:${POSTGRES_LISTENPORT}/${POSTGRES_DB}?user=${POSTGRES_USER}&password=${POSTGRES_PASSWORD}" && \
	python wait_for_db.py && \
	airflow db init && \
	airflow users create -u ${AIRFLOW_ADMIN_USER} -p ${AIRFLOW_ADMIN_PASSWORD} -r Admin -e admin@admin.com -f admin -l admin && \
	airflow webserver -D && \
	airflow scheduler
