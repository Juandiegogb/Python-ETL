from utils.config import getDBInfo
from sqlalchemy import create_engine, Connection, Engine
import pandas as pd
from utils.entities import ProcessedDf
from utils.entities import ValidationDBError
from pandas import DataFrame


class DB:

    connectionURL: str
    connection: Connection
    origin: bool
    df: DataFrame

    def __init__(self, variableName: str, origin=True):
        self.origin = origin
        dbInfo = getDBInfo(variableName)
        user = dbInfo["user"]
        password = dbInfo["password"]
        host = dbInfo["host"]
        port = dbInfo["port"]
        database = dbInfo["database"]
        engine = dbInfo["engine"]

        dbURL = {
            "postgres": f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}",
            "mysql": f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
            "mssql": f"mssql+pyodbc://{user}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server",
            "oracle": f"oracle+cx_oracle://{user}:{password}@{host}/{database}",
        }
        self.connectionURL = dbURL[engine]

        try:
            newEngine: Engine = create_engine(self.connectionURL)

            self.connection = newEngine.connect()
            print("DB connected")
        except Exception as e:
            print(f"Error al conectar a la base de datos:")
            raise

    def extract(self, query: str):
        try:
            print("Extracting data ....")
            df = pd.read_sql_query(query, self.connection)
            self.df = df
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
        finally:
            self.connection.close()

    def load(self, dataframes: list[ProcessedDf]):
        if self.origin:
            raise ValidationDBError("You are trying to load data to a origin database")
        else:
            for i in dataframes:
                df = i.dataframe
                tableName = i.destinyTableName

                try:
                    df.to_sql(
                        tableName, self.connection, if_exists="replace", index=False
                    )
                except Exception as e:
                    print("Error loading data to destiny database")
                    raise
            self.connection.close()
            print("Data loaded successfully")
