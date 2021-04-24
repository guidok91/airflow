# Sample Airflow setup with Docker
[Airflow](https://airflow.apache.org/) sample setup with Docker:
- Spins up one container for Airflow and one for its database (PostgreSQL).
- Uses LocalExecutor.

## Instructions
- Create `.env` file based on `.env.template`.
- Run `docker-compose up -d`.

Credentials for Airflow admin user are set on `.env` (`AIRFLOW_ADMIN_USER` and `AIRFLOW_ADMIN_PASSWORD`).
