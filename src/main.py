from utils.db import DB
from etl.extract import Extract
from etl.transform import Transform


def main():
    newDB = DB("postgres")
    connection = newDB.connect()
    query = "SELECT * FROM public.global_health_statistics"
    newExtraction = Extract(connection, query)
    df = newExtraction.getDataframe()
    newTransform = Transform(df)
    newTransform.exploreData()


main()
