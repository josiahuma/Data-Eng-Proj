from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from laptop_etl_proj.laptop_data import run_laptop_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023,12,30),
    'email': ['airflow@apache.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)

}

dag = DAG(
    'laptop_dag',
    default_args=default_args,
    description='laptop data dag'
)

run_etl = PythonOperator(
    task_id='complete_laptop_etl',
    python_callable=run_laptop_etl,
    dag=dag

)

run_etl