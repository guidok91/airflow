# Sample Airflow setup with Docker
[Apache Airflow](https://airflow.apache.org/) sample setup with Docker:
- Spins up one container for Airflow and one for its database (PostgreSQL).
- Uses [LocalExecutor](https://airflow.apache.org/docs/apache-airflow/stable/executor/local.html).

## Requirements
- [Docker](https://www.docker.com/).

## Instructions
- Create `.env` file based on `.env.template`.
- Run `make up`.

Credentials for Airflow admin user are set on `.env` (`AIRFLOW_ADMIN_USER` and `AIRFLOW_ADMIN_PASSWORD`).

Airflow UI is available on http://localhost:8080.
