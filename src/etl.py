import psycopg2.extensions as psyTypes
from utils.db import DBconnet
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
import numpy as np
from pandas import DataFrame
from utils.saveFile import saveFile


engine = DBconnet()


def extract(engine: Engine) -> pd.DataFrame:
    try:
        connection = engine.connect()
    except SQLAlchemyError as e:
        print(f"Database connection error: {e}")
        raise

    query = "SELECT * FROM public.global_health_statistics"

    try:
        print("Extracting data :) ...")
        df = pd.read_sql_query(query, connection)
        print("Data extracted successfully.")
        # df.info()
        saveFile(df.head(2), "head")
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        raise
    finally:
        connection.close()


def transform(df: DataFrame):
    # print(filtered_countries.head())
    country_counts = df.groupby("Country").size().reset_index(name="Record Count")
    saveFile(country_counts, "country_count")
    disease_count = df.groupby("Disease Name").size().reset_index(name="record_count")
    saveFile(disease_count, "disease_count")
    average_prevalence_data = df["Prevalence Rate (%)"].mean()
    min_val_prevalence = df["Prevalence Rate (%)"].min()
    max_val_prevalence = df["Prevalence Rate (%)"].max()

    country_max_prevalence = df.loc[df["Prevalence Rate (%)"].idxmax(), "Country"]
    stats_data = {
        "Statistic": [
            "Country with Max Prevalence",
            "Average Prevalence",
            "Min Prevalence",
            "Max Prevalence",
        ],
        "Value": [
            country_max_prevalence,
            average_prevalence_data,
            min_val_prevalence,
            max_val_prevalence,
        ],
    }
    stats_df = pd.DataFrame(stats_data)
    saveFile(stats_df, "prevalence_stats")
    print(average_prevalence_data)
    # print(disease_count)


def main():
    df = extract(engine)
    transform(df)


main()
