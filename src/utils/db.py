from sqlalchemy import create_engine
from utils.config import *


def DBconnet():
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )

    except Exception as e:
        print("Error al conectar a la base de datos:", e)
