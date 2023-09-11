"""
Stock Data Pipeline with Airflow

This module defines a DAG that manages a process for retrieving stock data
for predefined tickers using the `yfinance`package.
The pipeline checks if tables exist in the PostgreSQL database to store this data.
If not, it creates them.
Subsequently, the data is imported into the database tables.

DAG Structure:
1. Retrieve stock data.
2. Check if the database tables exist.
3. If tables don't exist, create them.
4. Import the stock data into the database.

Dependencies:
    - yfinance: to retrieve stock data.
    - psycopg2: for PostgreSQL connection and management.
    - airflow: for orchestrating the DAG.

Author: Chanyoung Park
Date: 2023-09-10
"""
from datetime import datetime
import yfinance as yf
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator


def retrieve_stock_data():
    """
    Retrieves stock data for predefined tickers between set start and end dates.

    Returns:
        dict: Dictionary with tickers as keys and their respective data as values.
    """
    tickers = ["VTI", "VEA", "VWO", "BND", "PDBC", "GLD", "VNQ", "EMLC"]
    data = {ticker: yf.download(
        ticker, start="2010-01-01", end="2023-12-31") for ticker in tickers}
    return data


def create_database_and_tables():
    """
    Connects to the airflow database and creates tables for predefined tickers if they don't exist.
    """
    conn = get_db_connection()
    with conn.cursor() as cursor:
        for ticker in ["VTI", "VEA", "VWO", "BND", "PDBC", "GLD", "VNQ", "EMLC"]:
            cursor.execute(f"SELECT to_regclass('public.{ticker.lower()}');")
            if not cursor.fetchone()[0]:
                cursor.execute(f"""
                CREATE TABLE {ticker.lower()} (
                    Date DATE PRIMARY KEY,
                    Open FLOAT NOT NULL,
                    High FLOAT NOT NULL,
                    Low FLOAT NOT NULL,
                    Close FLOAT NOT NULL,
                    Adj_Close FLOAT NOT NULL,
                    Volume INT NOT NULL
                );
                """)
        conn.commit()
    conn.close()


def import_data_to_db(connection, data_dict):
    """
    Imports stock data into the database.

    Args:
        connection (object): The database connection object.
        data_dict (dict): Dictionary containing stock data with tickers as keys
        and their respective data as values.
    """
    with connection.cursor() as cursor:
        for ticker, data_frame in data_dict.items():
            for _, row in data_frame.iterrows():
                cursor.execute(f"""
                INSERT INTO {ticker.lower()} (Date, Open, High, Low, Close, Adj_Close, Volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (Date) DO NOTHING;
                """, (row.name, row['Open'], row['High'],
                      row['Low'], row['Close'],
                      row['Adj Close'], int(row['Volume'])))
        connection.commit()


def get_db_connection():
    """
    Returns a connection to the airflow database.

    Returns:
        object: Database connection object.
    """
    return psycopg2.connect(host="postgres", dbname="airflow", user="airflow", password="airflow")


def check_table_existence(**kwargs):
    """
    Checks the existence of the 'vti' table in the airflow database
    and determines the next task in the DAG.

    Args:
        **kwargs: Contains 'task_instance' for xcom operations.

    Returns:
        str: Task id of the next task to be executed.
    """
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT to_regclass('public.vti');")
        table_exists = cursor.fetchone()[0]
    conn.close()
    kwargs['task_instance'].xcom_push(key='table_exists', value=table_exists)
    return 'create_tables' if not table_exists else 'import_data'


def import_data(**kwargs):
    """
    Imports stock data retrieved from the 'retrieve_stock_data' task into the database.

    Args:
        **kwargs: Contains 'task_instance' for xcom operations.
    """
    task_instance = kwargs['task_instance']
    data = task_instance.xcom_pull(task_ids='retrieve_stock_data')
    conn = get_db_connection()
    import_data_to_db(conn, data)
    conn.close()


default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 13),
    'retries': 1
}

dag = DAG(
    'stock_data_pipeline',
    default_args=default_args,
    description='A DAG to retrieve stock data and store it in a database',
    schedule_interval=None
)

retrieve_task = PythonOperator(
    task_id='retrieve_stock_data',
    python_callable=retrieve_stock_data,
    provide_context=True,
    dag=dag
)
table_check_task = BranchPythonOperator(
    task_id='check_table_existence',
    python_callable=check_table_existence,
    provide_context=True,
    dag=dag
)
create_tables_task = PythonOperator(
    task_id='create_tables',
    python_callable=create_database_and_tables,
    dag=dag
)
import_data_task = PythonOperator(
    task_id='import_data',
    python_callable=import_data,
    provide_context=True,
    dag=dag
)

retrieve_task >> table_check_task >> [create_tables_task, import_data_task]
create_tables_task >> import_data_task
