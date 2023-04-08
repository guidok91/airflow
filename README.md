# Sample Airflow setup with Kubernetes
[Apache Airflow](https://airflow.apache.org/) sample setup with Kubernetes.

Spins up a local Kubernetes cluster for Airflow with Kind:
  - Uses a PosgreSQL database for Airflow.
  - Uses [Kubernetes Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html) to run each Airflow task on an isolated pod.

This is meant as a sample local setup. In order to run it in a production environment, please refer to the [Airflow Helm chart production guide](https://airflow.apache.org/docs/helm-chart/stable/production-guide.html).

## Requirements
[Kind](https://kind.sigs.k8s.io/), [Docker](https://www.docker.com/) and [Helm](https://helm.sh/) for local Kubernetes cluster.

## Instructions
The repo includes a `Makefile`. You can run `make help` to see usage.

Basic setup:
- Run `make k8s-cluster-up` to spin up local Kubernetes cluster with Kind.
- Run `make add-airflow-helm-chart` to add the official Airflow Helm chart to the local repo.
- Run `make k8s-create-airflow-namespace` to create a namespace for the Airflow deployment.
- Run `make airflow-k8s-up` to deploy Airflow on the local Kubernetes cluster.
- On a separate terminal, run `make airflow-webserver-port-forward` to be able to access the Airflow webserver on http://localhost:8080.

The credentials for the webserver are admin/admin.

If you need to customize [Airflow configuration](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html) you can add the corresponding env variables under `env` in [values.yaml](values.yaml).  
