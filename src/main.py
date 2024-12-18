from utils.db import DB
from etl.extract import Extract
from etl.transform import Transform
from etl.load import Load


def main():
    print("ETL started")
    originDB = DB("postgres")
    originConnection = originDB.connect()
    query = "SELECT * FROM public.global_health_statistics"
    newExtraction = Extract(originConnection, query)
    df = newExtraction.getDataframe()

    newTransform = Transform(df)
    newTransform.exploreData()
    transformedDataframes = newTransform.transformData()

    destinyDB = DB("postgres")
    destinyConnection = destinyDB.connect()
    newLoad = Load(destinyConnection, transformedDataframes)


main()
