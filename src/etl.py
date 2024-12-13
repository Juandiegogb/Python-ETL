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


def test():
    data = {
        "nombre": ["Juan", "Diego", "Miguel", "Maria", "Sara"],
        "carrera": ["Sistemas", "Medicina", "Medicina", "Economia", "Gastronomia"],
        "email": [
            "juan@gmail.com",
            "diego@gmail.com",
            "miguel@gmail.com",
            "maria@gmail.com",
            "sara@gmail.com",
        ],
    }

    df = pd.DataFrame(data)
    df.to_csv("./processed_data/test.csv")
    print(df)


def test2():
    df = pd.DataFrame(
        [["Juan", 21], ["Maria", 23], ["Sara", 23]], columns=["Nombre", "Edad"]
    )
    df.info()

    df.to_csv("./processed_data/test2.csv")


def test3():
    df = pd.DataFrame(np.random.randn(4, 3), columns=["a", "b", "c"])
    df.to_csv("./processed_data/numpy.csv")


test()
test2()
test3()
