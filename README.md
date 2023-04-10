# Sample Airflow setup with Kubernetes
[Apache Airflow](https://airflow.apache.org/) sample setup with Kubernetes.

Spins up a local Kubernetes cluster for Airflow with Kind:
  - Uses a PostgreSQL database for Airflow.
  - Uses [Kubernetes Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html) to run each Airflow task on an isolated pod.

This is meant as a sample local setup. In order to run it in a production environment, please refer to the [Airflow Helm chart production guide](https://airflow.apache.org/docs/helm-chart/stable/production-guide.html).

## Requirements
[Kind](https://kind.sigs.k8s.io/), [Docker](https://www.docker.com/) and [Helm](https://helm.sh/) for local Kubernetes cluster.

## Instructions
The repo includes a `Makefile`. You can run `make help` to see usage.

Basic setup:
- Run `make k8s-cluster-up` to spin up local Kubernetes cluster with Kind.
- Run `make airflow-k8s-add-helm-chart` to add the official Airflow Helm chart to the local repo.
- Run `make airflow-k8s-create-namespace` to create a namespace for the Airflow deployment.
- Run `make airflow-k8s-up` to deploy Airflow on the local Kubernetes cluster.
- On a separate terminal, run `make airflow-webserver-port-forward` to be able to access the Airflow webserver on http://localhost:8080.

The credentials for the webserver are admin/admin.

## Configuration
If you need to customize [Airflow configuration](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html) you can edit the `config` section in [values.yaml](k8s/values.yaml).

Also environment variables can be added in the `env` section (they will be present in all the pods). 

## DAG deployment
DAGs are deployed via GitSync.

GitSync acts as a side car container alongside the other Airflow pods, synchronising the `dags/` folder in the pods with the DAGs located in a Git repo of your choice (in this case https://github.com/guidok91/airflow/tree/master/dags).

## Custom Docker image for pods
A custom [Docker image](Dockerfile) is provided for the pods. Here we can install the Airflow dependencies we need.

## Logs
So that Airflow logs don't get lost every time a task finishes (e.g. the pod gets deleted), the setup provides a [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) that shares the logs with the host system in the `data/` folder.
