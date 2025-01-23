from pyspark.sql import SparkSession
from objects.custom import custom


class Etl:
    def __init__(self):
        self.spark: SparkSession = SparkSession.builder.appName("Etl").getOrCreate()

    def extract(self, origin_db_url: str, destiny_db_url: str, tables: list[str]):
        spark = self.spark
        if origin_db_url == destiny_db_url:
            raise ValueError("Origin DB and destiny are the same db")

        data: list[custom] = [
            custom(table, spark.read.jdbc(origin_db_url, table)) for table in tables
        ]

        for i in data:
            table_name = i.cleaned_name
            df = i.dataframe
            df.write.jdbc(destiny_db_url, table_name)
