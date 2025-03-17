import geopandas as gpd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import glob


load_dotenv()

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_DATABASE')

engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')

geojson_folder = './data'

geojson_files = glob.glob(os.path.join(geojson_folder, '*.geojson'))

for filepath in geojson_files:
    gdf = gpd.read_file(filepath)
    table_name = os.path.basename(filepath).split('.')[0]
    gdf.to_postgis(table_name, engine, if_exists='replace')
    print(f'Imported {table_name} to database')

