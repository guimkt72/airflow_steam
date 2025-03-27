from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.db_connection import load_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dbt_pipeline',
    default_args=default_args,
    description='Pipeline de ETL com dbt',
    schedule_interval='@daily',
    catchup=False
)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=load_data,
    dag=dag,
)

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='''
    cd /usr/local/airflow/airflow_steam && \
    dbt clean && \
    dbt deps && \
    dbt run --profiles-dir=/usr/local/airflow/airflow_steam || \
    (echo "DBT failed, running debug..." && dbt debug --profiles-dir=/usr/local/airflow/airflow_steam && exit 1)
    ''',
    dag=dag,
)

dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command='''
    cd /usr/local/airflow/airflow_steam && \
    dbt test
    ''',
    dag=dag,
)

extract_task >> dbt_run >> dbt_test