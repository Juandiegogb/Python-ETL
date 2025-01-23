import csv
from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from utils.config import get_url
from time import time
from pyspark.errors.exceptions.base import AnalysisException

# Start the Spark session
spark: SparkSession = (
    SparkSession.builder.appName("etl")
    .config("spark.driver.memory", "5g")
    .getOrCreate()
)

started_at = time()
origin_db = get_url("ORIGIN_DB")
stage_db = get_url("TEST_BI")

# Read the CSV file and prepare the tables
with open("tables.csv", "r", encoding="UTF-8") as file:
    data = list(csv.reader(file))
    print(len(data))

    # Initialize list to store table data
    not_found_col = []

    # For parallel execution, let's directly map the table names and columns
    for row in data:
        name = row[0]
        columns = [col for col in row[1].strip().split(" ") if col]

        if columns:
            try:
                # Using `select` with specified columns directly in the query
                dataframe = spark.read.jdbc(origin_db, name, columns=columns)
            except AnalysisException as e:
                not_found_col.append(e.getMessageParameters()["objectName"])
                continue
        else:
            # Read without columns if the list is empty
            dataframe = spark.read.jdbc(origin_db, name)

        # Write to the target database
        try:
            dataframe.write.jdbc(
                stage_db,
                f"pyspark_{name.strip().upper()}",
                mode="overwrite",
                numPartitions=10,  # Optional: Partitioning can speed up the write process
                properties={"driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"},
            )
        except Py4JJavaError:
            print(dataframe.printSchema())
        except AttributeError:
            continue

# Print total time
total_time = round(time() - started_at)
print(f"This job took {total_time} seconds")
print(not_found_col)
