import csv
from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from utils.config import get_url
from time import time, sleep
from pyspark.errors.exceptions.base import AnalysisException

# Start the Spark session
spark: SparkSession = (
    SparkSession.builder.appName("etl")
    .config("spark.executor.cores", "1")
    .master("spark://132.147.2.201:7077")
    .getOrCreate()
)

started_at = time()
origin_db = get_url("ORIGIN_DB")
stage_db = get_url("TEST_BI")


with open("tables.txt", "r", encoding="UTF-8") as file:
    data = set(file.readlines())

    not_found_col = []

    for row in data:
        name = row[0]
        columns = [col for col in row[1].strip().split(" ") if col]

        if columns:
            try:
                dataframe = spark.read.jdbc(origin_db, name, numPartitions=10).select(
                    columns
                )
            except AnalysisException as e:
                not_found_col.append(e.getMessageParameters()["objectName"])
                continue
        else:
            dataframe = spark.read.jdbc(origin_db, name)

        try:
            dataframe.printSchema()
            dataframe.write.jdbc(
                stage_db,
                f"pyspark_{name.strip().upper()}",
                mode="overwrite",
            )
        except Py4JJavaError:
            print(dataframe.printSchema())
        except AttributeError:
            continue


total_time = round(time() - started_at)
print(f"This job took {total_time} seconds")
print(not_found_col)
