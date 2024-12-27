from etl.db import DB
from etl.transform import Transform


def main():
    print("ETL started")
    originDB = DB("DB_ORIGIN")
    query = "SELECT * FROM public.global_health_statistics"
    originDB.extract(query)
    
    newTransform = Transform(originDB.df)
    newTransform.exploreData()
    transformedDataframes = newTransform.transformData()

    destinyDB = DB("DB_DESTINY", False)
    destinyDB.load(transformedDataframes)




# main()
print("hola")
