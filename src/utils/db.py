import psycopg2 as ps2
from utils.config import database, user, password, host, port
import sqlalchemy as sqla
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def DBconnet() -> Engine:
    try:
        engine: Engine = create_engine(
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )
        return engine
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise
