init:
	pip install --upgrade pip setuptools && pip install -r requirements.txt

init_airflow:
	airflow db init
	airflow users create -u ${AIRFLOW_ADMIN_USER} -p ${AIRFLOW_ADMIN_PASSWORD} -r Admin -e admin@admin.com -f admin -l admin

run:
	airflow webserver -D
	airflow scheduler
