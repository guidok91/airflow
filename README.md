# Airflow sample project
Docker image containing an Airflow setup with Local Executor (PostgreSQL).  

## Setup
- Create `.env` file based on `.env.template`.
- Run `docker-compose up -d`.
- Credentials for Airflow Webserver are set on `.env` (`AIRFLOW_ADMIN_USER` and `AIRFLOW_ADMIN_PASSWORD`).
