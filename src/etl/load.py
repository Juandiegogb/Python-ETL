from sqlalchemy import Connection
from utils.entities import ProcessedDf


class Load:
    def __init__(self, connection: Connection, dataframes: list[ProcessedDf]):
        for i in dataframes:
            df = i.dataframe
            tableName = i.destinyTableName
            df.to_sql(tableName, connection)
