import os
import time
import logging
import pandas as pd
import sqlalchemy

logging.basicConfig(level=logging.INFO)

conn_string = os.environ["AIRFLOW__CORE__SQL_ALCHEMY_CONN"]
retries = 10

while retries > 0:
    try:
        logging.info("Trying to connect to AirflowDB...")
        pd.read_sql("select 1;", conn_string)
        logging.info("Airflow DB is up!")
        break
    except sqlalchemy.exc.OperationalError as e:
        logging.warning(f"Cannot connect to Airflow DB\n"
                        f"The error is: {str(e)}\n"
                        f"Trying again (retries left {retries})...")
        time.sleep(3)
        retries = retries - 1
        continue

if retries == 0:
    raise Exception("Could not connect to Airflow DB")
