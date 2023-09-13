"""
Stock Data Pipeline with Airflow

This module defines a DAG that manages a process for retrieving stock data
for predefined tickers using the `yfinance`package.
The pipeline checks if tables exist in the PostgreSQL database to store this data.
If not, it creates them.
Subsequently, the data is imported into the database tables.

DAG Structure:
1. Check if the database tables exist.
2. If tables don't exist, create them.


Dependencies:
    - psycopg2: for PostgreSQL connection and management.
    - airflow: for orchestrating the DAG.

Author: Chanyoung Park
Date: 2023-09-12
"""
from datetime import timedelta
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
from airflow.exceptions import AirflowException


def create_database_and_tables():
    """
    Connects to the airflow database and creates tables for predefined tickers if they don't exist.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT to_regclass('public.stock_data');")
            if not cursor.fetchone()[0]:
                cursor.execute("""
                CREATE TABLE stock_data (
                    Date DATE NOT NULL,
                    stock_code VARCHAR(5) NOT NULL,
                    Open FLOAT NOT NULL,
                    High FLOAT NOT NULL,
                    Low FLOAT NOT NULL,
                    Close FLOAT NOT NULL,
                    Adj_Close FLOAT NOT NULL,
                    Volume INT NOT NULL,
                    PRIMARY KEY(Date, stock_code)
                );
                """)
            conn.commit()


def get_db_connection():
    """
    Returns a connection to the airflow database.

    Returns:
        object: Database connection object.
    """
    try:
        return psycopg2.connect(
            host="postgres", dbname="airflow",
            user="airflow", password="airflow"
        )
    except Exception as error:
        raise AirflowException(
            f"Failed to connect to the database due to {error}") from error


def check_table_existence(**kwargs):
    """
    Checks the existence of the 'vti' table in the airflow database
    and determines the next task in the DAG.

    Args:
        **kwargs: Contains 'task_instance' for xcom operations.

    Returns:
        str: Task id of the next task to be executed.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT to_regclass('public.stock_data');")
            table_exists = cursor.fetchone()[0]
    kwargs['task_instance'].xcom_push(key='table_exists', value=table_exists)


default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 3,   # Increase retries
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': ['chanyoung.p.1988@gmail.com']
}


dag = DAG(
    'stock_data_pipeline',
    default_args=default_args,
    description='A DAG to create stock data table in a database'
)

table_check_task = PythonOperator(
    task_id='check_table_existence',
    python_callable=check_table_existence,
    provide_context=True,
    dag=dag
)

create_tables_task = PythonOperator(
    task_id='create_tables',
    python_callable=create_database_and_tables,
    trigger_rule=TriggerRule.ALL_FAILED,  # Only create if table_check_task fails
    dag=dag
)

table_check_task >> create_tables_task
