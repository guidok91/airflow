FROM apache/airflow:2.5.3

USER root
RUN apt-get update -q -y && \
    apt-get install -y vim make build-essential libpq-dev && \
    apt-get clean -q -y && \
    apt-get autoclean -q -y && \
    apt-get autoremove -q -y

USER airflow
RUN pip install --upgrade pip setuptools wheel astronomer-providers[apache.livy]~=1.15.2
