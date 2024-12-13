import pandas as pd
from pandas import DataFrame


def saveFile(dataframe: DataFrame, name: str) -> None:
    dataframe.to_csv(f"./processed_data/{name}.csv")
