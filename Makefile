.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY:
k8s-cluster-up: # Create local Kubernetes cluster.
	kind create cluster --name airflow-cluster --config k8s/kind-cluster.yaml

.PHONY:
k8s-cluster-down: # Tear down local Kubernetes cluster.
	kind delete cluster --name airflow-cluster

.PHONY:
airflow-k8s-add-helm-chart: # Add official Airflow Helm chart to local repository.
	helm repo add apache-airflow https://airflow.apache.org
	helm repo update

.PHONY:
airflow-k8s-create-namespace: # Creates Kubernetes namespace for Airflow.
	kubectl create namespace airflow

.PHONY:
airflow-k8s-up: # Deploy Airflow on local Kubernetes cluster.
	docker build -t airflow-custom:1.0.0 .
	kind load docker-image airflow-custom:1.0.0 --name airflow-cluster
	helm upgrade --install airflow apache-airflow/airflow -n airflow -f k8s/values.yaml --version 1.9.0 --debug
	kubectl apply -f k8s/persistent-volume.yaml
	kubectl apply -f k8s/persistent-volume-claim.yaml

.PHONY:
airflow-k8s-down: # Tear down Airflow deployment on local Kubernetes cluster.
	helm delete airflow --namespace=airflow

.PHONY:
airflow-webserver-port-forward: # Make Airflow webserver accessible on http://localhost:8080.
	kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow

.PHONY:
dev-env-up: # Create local virtual env to develop DAG code.
	python -m venv .venv
	. .venv/bin/activate && \
	pip install --upgrade pip setuptools wheel && \
	pip install -r requirements-dev.txt && \
	pip install -r requirements.txt

.PHONY:
test: # Run tests for DAG code.
	. .venv/bin/activate && \
	pytest tests
