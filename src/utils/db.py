from utils.config import user, password, port, database, host
from sqlalchemy import create_engine
from sqlalchemy import Connection
from utils.entities import serverOptions


class DB:

    connectionURL: str

    def __init__(self, server: serverOptions):
        dbURL = {
            "postgres": f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}",
            "mysql": f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
            "mssql": f"mssql+pyodbc://{user}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server",
            "oracle": f"oracle+cx_oracle://{user}:{password}@{host}:{port}/{database}",
        }
        self.connectionURL = dbURL[server]

    def connect(self) -> Connection:
        try:
            engine = create_engine(self.connectionURL)
            connection: Connection = engine.connect()
            print("DB connected")
            return connection
        except Exception as e:
            print(f"Error al conectar a la base de datos:")
            raise
