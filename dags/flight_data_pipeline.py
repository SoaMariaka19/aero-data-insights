from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from scripts.extract_data import extract_airport_city_search

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'flight_data_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_airport_city_search,
    dag=dag,
)

def run_notebook():
    import nbformat
    from nbconvert import PythonExporter

    with open('dags/notebook/extraction_destination.ipynb', 'r') as f:
        notebook_content = f.read()

    notebook = nbformat.reads(notebook_content, as_version=4)
    exporter = PythonExporter()
    python_code, _ = exporter.from_notebook_node(notebook)

    exec(python_code)

run_notebook_task = PythonOperator(
    task_id='run_notebook',
    python_callable=run_notebook,
    dag=dag,
)

store_to_s3_task = BashOperator(
    task_id='store_to_s3',
    bash_command='aws s3 cp /data/data.csv s3://your-bucket-name/{{ ds }}/file.csv',
    dag=dag,
)

extract_task >> run_notebook_task >> store_to_s3_task
