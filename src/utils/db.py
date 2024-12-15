from utils import config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def DBconnet() -> Engine:
    try:
        engine: Engine = create_engine(
            f"postgresql+psycopg2://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"
        )
        return engine
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise
