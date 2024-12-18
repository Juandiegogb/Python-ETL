from utils.db import DB
from etl.extract import Extract
from etl.transform import Transform
from etl.load import Load


def main():
    print("ETL started")
    originDB = DB("DB_ORIGIN")
    originConnection = originDB.connect()
    query = "SELECT * FROM public.global_health_statistics"
    newExtraction = Extract(originConnection, query)
    df = newExtraction.getDataframe()

    newTransform = Transform(df)
    newTransform.exploreData()
    transformedDataframes = newTransform.transformData()

    destinyDB = DB("DB_DESTINY")
    destinyConnection = destinyDB.connect()
    newLoad = Load(destinyConnection, transformedDataframes)


main()
