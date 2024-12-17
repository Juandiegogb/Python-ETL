from pandas import DataFrame


class Transform:

    df: DataFrame

    def __init__(self, dataframe: DataFrame):
        self.df = dataframe

    def exploreData(self):
        df = self.df
        df.info()
        print(df.shape)
        print(df.describe())
