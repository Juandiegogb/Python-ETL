import pandas as pd

df = pd.read_csv("./data.csv", delimiter=",", encoding="unicode_escape")
print(df)
