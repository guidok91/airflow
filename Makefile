up:
	docker-compose up -d

down:
	docker-compose rm -fs

setup:
	pip install --upgrade pip setuptools && pip install -r requirements.txt

airflow_start:
	python wait_for_db.py
	airflow db init
	airflow users create -u ${AIRFLOW_ADMIN_USER} -p ${AIRFLOW_ADMIN_PASSWORD} -r Admin -e admin@admin.com -f admin -l admin
	airflow webserver -D
	airflow scheduler
