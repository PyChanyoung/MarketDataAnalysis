"""
Stock Data Pipeline with Airflow

This module defines a DAG that manages a process for retrieving stock data
for predefined tickers using the `yfinance` package.
The pipeline then imports the retrieved data into the PostgreSQL database.

DAG Structure:
1. Retrieve stock data.
2. Import the stock data into the database.

Dependencies:
    - yfinance: to retrieve stock data.
    - psycopg2: for PostgreSQL connection and management.
    - airflow: for orchestrating the DAG.

Author: Chanyoung Park
Date: 2023-09-12
"""

from datetime import timedelta
import yfinance as yf
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.exceptions import AirflowException


def retrieve_stock_data():
    """
    Retrieves stock data for predefined tickers between set start and end dates.

    Returns:
        dict: Dictionary with tickers as keys and their respective data as values.
    """
    tickers = ["VTI", "VEA", "VWO", "BND", "PDBC", "GLD", "VNQ", "EMLC"]
    try:
        data = {ticker: yf.download(
            ticker, start="2010-01-01", end="2023-12-31") for ticker in tickers}
    except Exception as error:
        raise AirflowException(
            f"Failed to retrieve stock data due to {error}") from error
    return data


def import_data_to_db(connection, data_dict):
    """
    Imports stock data into the database.

    Args:
        connection (object): The database connection object.
        data_dict (dict): Dictionary containing stock data with tickers as keys
        and their respective data as values.
    """
    try:
        with connection.cursor() as cursor:
            for stock_code, data_frame in data_dict.items():
                for _, row in data_frame.iterrows():
                    cursor.execute("""
                    INSERT INTO stock_data (Date, stock_code, Open, High, Low, Close, Adj_Close, Volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (Date, stock_code) DO NOTHING;
                    """, (row.name, stock_code, row['Open'], row['High'],
                          row['Low'], row['Close'],
                          row['Adj Close'], int(row['Volume'])))
            connection.commit()
    except Exception as error:
        raise AirflowException(
            f"Failed to import stock data to the database due to {error}") from error


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


def import_data(**kwargs):
    """
    Imports stock data retrieved from the 'retrieve_stock_data' task into the database.

    Args:
        **kwargs: Contains 'task_instance' for xcom operations.
    """
    task_instance = kwargs['task_instance']
    data = task_instance.xcom_pull(task_ids='retrieve_stock_data')
    with get_db_connection() as conn:
        import_data_to_db(conn, data)


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
    description='A DAG to retrieve stock data and store it in a database',
    schedule_interval='@daily'
)

retrieve_task = PythonOperator(
    task_id='retrieve_stock_data',
    python_callable=retrieve_stock_data,
    provide_context=True,
    dag=dag
)

import_data_task = PythonOperator(
    task_id='import_data',
    python_callable=import_data,
    provide_context=True,
    dag=dag
)

retrieve_task >> import_data_task
