from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG

from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

from os.path import basename, splitext
file_name = splitext(basename(__file__))[0]

with DAG(
    file_name,
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 2, 5),
    catchup=False,
    tags=['example'],
) as dag:
    t1 = BashOperator(
            task_id='print_date',
            bash_command='date'
        )
    t2 = BashOperator(
            task_id='sleep',
            depends_on_past=False,
            bash_command='sleep 5',
            retries=3,
        )

    t1.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)

    """)
    dag.doc_md = __doc__
    dag.doc_md = """this is a documentation placed anywhere"""

    template_command = dedent(
        """
            {% for i in range(5) %}
                echo "{{ ds }}"
                echo "{{ macros.ds_add(ds, 7)}}"
                echo "{{ params.my_param }}"
            {% endfor %}
        """
    )

    t3 = BashOperator(
        task_id='hello_world',
        depends_on_past=False,
        bash_command=template_command,
        params={'my_param': 'Parameter I Passed in'},
    )
    t1 >> [t2, t3]
