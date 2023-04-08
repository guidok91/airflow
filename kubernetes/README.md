# Sample Airflow setup with Docker
[Apache Airflow](https://airflow.apache.org/) sample setup with Kubernetes:
- Spins up a local Kubernetes cluster for Airflow with Kind:
    - Uses a local PosgreSQL database for Airflow.
    - Uses [Kubernetes Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html) to run each Airflow task on an isolated pod.

## Requirements
[Kind](https://kind.sigs.k8s.io/), [Docker](https://www.docker.com/) and [Helm](https://helm.sh/) for local Kubernetes cluster.

## Instructions

## Caveats
- The current setup includes a PostgreSQL deployment in Kubernetes. In a production environment, the Airflow database should be hosted separately (for example as a AWS RDS instance).
