import psycopg2.extensions as psyTypes
from utils.db import DBconnet
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
import numpy as np


engine = DBconnet()


def extract(engine: Engine) -> pd.DataFrame:
    try:
        connection = engine.connect()
    except SQLAlchemyError as e:
        print(f"Database connection error: {e}")
        raise

    query = "SELECT * FROM public.global_health_statistics"

    try:
        df = pd.read_sql_query(query, connection)
        print("Data extracted successfully.")
        df.info()
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        raise
    finally:
        connection.close()



extract(engine)
