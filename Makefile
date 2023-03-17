.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY:
docker-up: # Spin up local Airflow in Docker.
	docker-compose up -d

.PHONY:
docker-down: # Tear down local Airflow.
	docker-compose down

.PHONY:
docker-rm: # Remove local Docker images.
	docker-compose rm -fs

.PHONY:
docker-build: # Build local Docker images.
	docker-compose build

.PHONY:
setup: # Install Python dependencies.
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

.PHONY:
airflow-start: # Start Airflow services.
	python wait_for_db.py
	airflow db init
	airflow users create -u ${AIRFLOW_ADMIN_USER} -p ${AIRFLOW_ADMIN_PASSWORD} -r Admin -e admin@admin.com -f admin -l admin
	airflow webserver -D
	airflow scheduler
