from sqlalchemy import Connection
from utils.entities import ProcessedDf


class Load:
    def __init__(self, connection: Connection, dataframes: list[ProcessedDf]):
        for i in dataframes:
            df = i.dataframe
            tableName = i.destinyTableName

            try:
                df.to_sql(tableName, connection, if_exists="replace", index=False)
            except Exception as e:
                print("Error loading data to destiny database")
                raise
        connection.close()
        print("Data loaded successfully")
