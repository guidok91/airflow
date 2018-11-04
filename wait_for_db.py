import pandas as pd
import os
import sqlalchemy
import time

# Wait for Airflow DB to be ready

conn_string = os.environ['AIRFLOW__CORE__SQL_ALCHEMY_CONN']
error = True

while error:
    try:
        print('Trying to connect to AirflowDB...')
        pd.read_sql('select 1;', conn_string)
        print('AirflowDB is up!')
        error = False
    except sqlalchemy.exc.OperationalError as e:
        print("Cannot connect to Airflow DB with connection string: {}\nThe error is: {}\nTrying again..."
              .format(conn_string, str(e)))
        time.sleep(3)
        continue
