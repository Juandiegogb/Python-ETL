import os
from dotenv import load_dotenv

load_dotenv()

data_dir = "/data"
os.makedirs(data_dir, exist_ok=True)

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")
