from typing import NamedTuple, TypedDict
from pandas import DataFrame


class ProcessedDf(NamedTuple):
    dataframe: DataFrame
    destinyTableName: str


class DBConfig(TypedDict):
    host: str
    port: int
    user: str
    password: str
    database: str
    engine: str
