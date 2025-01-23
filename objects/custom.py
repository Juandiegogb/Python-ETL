from pyspark.sql import DataFrame


class custom:
    def __init__(self, name: str, columns: list[str], dataframe: DataFrame = None):
        self.dataframe: DataFrame = dataframe
        self.original_name: str = name
        self.cleaned_name: str = f"pyspark_{name.strip().upper()}"
        self.columns: list[str] = columns

    def __str__(self):
        return f"{self.cleaned_name}: {self.columns} "
