FROM python:3.9-slim

RUN apt-get update -q -y && \
    apt-get install -y vim make build-essential && \
    apt-get clean -q -y && \
    apt-get autoclean -q -y && \
    apt-get autoremove -q -y

ENV AIRFLOW_HOME="/airflow"
ENV PYTHONPATH="$PYTHONPATH:$AIRFLOW_HOME" \
    AIRFLOW__CORE__EXECUTOR=LocalExecutor \
    AIRFLOW__CORE__LOAD_EXAMPLES=False

COPY ./dags $AIRFLOW_HOME/dags
COPY ["wait_for_db.py", "requirements.txt", "Makefile", "$AIRFLOW_HOME/"]

WORKDIR $AIRFLOW_HOME

RUN make setup

CMD make airflow-start
