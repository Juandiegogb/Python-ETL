import pandas as pd
from sqlalchemy import Connection
from pandas import DataFrame


class Extract:
    df: DataFrame

    def __init__(self, connection: Connection, query: str):
        try:
            print("Extracting data ....")
            df = pd.read_sql_query(query, connection)
            self.df = df
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
        finally:
            connection.close()

    def getDataframe(self) -> DataFrame:
        return self.df
