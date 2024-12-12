import psycopg2.extensions as psyTypes
from utils.db import DBconnet
import pandas as ps
from sqlalchemy.engine import Engine


engine = DBconnet()


def extract(engine: Engine) -> None:

    try:
        connection = engine.connect()
    except Exception as e:
        print(e)
        raise

    query = "SELECT * FROM public.global_health_statistics"

    df = ps.read_sql_query(query, connection)
    # print(dataframe.head())
    df.info()
    print(df.head())
    print("Done")
    connection.close()


extract(engine)
