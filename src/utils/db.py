from utils import config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def DBconnet(server: str) -> Engine:
    dbURL = {
        "postgresql": f"postgresql+psycopg2://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}",
        "mysql": f"mysql+pymysql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}",
        "mssql": f"mssql+pyodbc://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}?driver=ODBC+Driver+17+for+SQL+Server",
        "oracle": f"oracle+cx_oracle://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}",
    }
    try:
        engine: Engine = create_engine(dbURL[server])
        return engine
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise
