from pandas import DataFrame
from utils.entities import ProcessedDf


class Transform:

    df: DataFrame

    def __init__(self, dataframe: DataFrame):
        self.df = dataframe

    def exploreData(self):
        df = self.df
        df.info()
        print(df.shape)
        print(df.describe())

    def transformData(self) -> list[ProcessedDf]:
        df = self.df
        DfArray: list[ProcessedDf]
        DfArray.append(ProcessedDf(df.describe(), "description"))
        return DfArray
