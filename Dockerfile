FROM apache/airflow:2.6.1

USER root

COPY .logs/ /opt/airflow/logs
COPY airflow/dags/ /opt/airflow/dags
COPY airflow/plugins/ /opt/airflow/plugins
COPY airflow/data/ /opt/airflow/data

COPY requirements.txt /opt/airflow/requirements.txt
COPY airflow_config/airflow.cfg /opt/airflow/airflow.cfg

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    gcc \   
    && apt-get clean

RUN apt-get install -y gcc make apt-transport-https ca-certificates build-essential

ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow/plugins"
ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow/data"
ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow"

USER airflow
# RUN chown airflow  /opt/airflow/airflow.cfg

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --upgrade wheel
RUN pip install -r requirements.txt