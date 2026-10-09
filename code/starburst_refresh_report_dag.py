"""Airflow DAG: send the Starburst refresh report every day at 9:00 AM IST."""
from datetime import datetime, timedelta

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

REPORT_DIR = "/opt/airflow/scripts/starburst_report"   # where the script + config live

with DAG(
    dag_id="starburst_last_refresh_report",
    start_date=pendulum.datetime(2026, 10, 1, tz="Asia/Kolkata"),
    schedule="0 9 * * *",
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=10)},
    tags=["starburst", "monitoring"],
) as dag:
    BashOperator(
        task_id="send_refresh_report",
        bash_command=f"cd {REPORT_DIR} && python starburst_refresh_report.py --config config.yaml",
        # STARBURST_PASSWORD / SMTP_PASSWORD: inject from Airflow Variables/Connections or a secrets backend
    )
