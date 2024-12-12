from sqlalchemy import create_engine
from config import user, password, host, port, database

try:

    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )
    with engine.connect() as connection:
        print("DB connected")
except Exception as e:
    print("Error al conectar a la base de datos:", e)
