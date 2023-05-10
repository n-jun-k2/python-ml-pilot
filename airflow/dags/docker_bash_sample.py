from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta
from os.path import basename, splitext
from click import command

from pydata_google_auth import default


file_name = splitext(basename(__file__))[0]
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2022, 2, 6),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}



with DAG(file_name, default_args=default_args, schedule_interval=timedelta(1)) as dag:
    t1 = BashOperator(
        task_id="print_start",
        bash_command="""
            echo $(date '+%Y-%m-%d %H:%M:%S') started.
        """
    )

    t2 = DockerOperator(
        task_id="docker_command",
        image='centos:latest',
        api_version='auto',
        auto_remove=True,
        command="""/bin/bash -c \'echo "1" && sleep 30 && echo "2"\'""",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )