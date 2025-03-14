import os
from dotenv import load_dotenv
from langchain.sql_database import SQLDatabase

load_dotenv()

def get_sql_database():
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    database = os.getenv('DB_DATABASE')

    uri = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
    return SQLDatabase.from_uri(uri)


