from typing import Literal, NamedTuple
from pandas import DataFrame


class ProcessedDf(NamedTuple):
    dataframe: DataFrame
    destinyTableName: str


serverOptions = Literal["postgres", "mysql", "oracle", "mssql"]
