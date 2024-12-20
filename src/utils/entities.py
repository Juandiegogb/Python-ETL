from typing import NamedTuple, TypedDict
from pandas import DataFrame
import logging


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


class ValidationDBError(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
        logging.warning(self.message)
