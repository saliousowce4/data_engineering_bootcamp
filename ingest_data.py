import  os
import pandas as pd
from sqlalchemy import create_engine

DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "ny_taxi"

URL_TAXI = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
URL_ZONES = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

def main():
    connection_string = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    engine = create_engine(connection_string)

    print("Connection established")

    print(f"Downloading Zones from {URL_ZONES}...")

    df_zones = pd.read_csv(URL_ZONES)

    df_zones.to_sql(name='zones', con=engine, if_exists='replace')

    print("Zones ingested successfully.")

    print(f"Downloading Taxi Data from {URL_TAXI}...")

    df_taxi = pd.read_parquet(URL_TAXI)

    df_taxi.head(n=0).to_sql(name='green_taxi_trips', con=engine, if_exists='replace')

    df_taxi.to_sql(name='green_taxi_trips', con=engine, if_exists='append', chunksize=100000)

    print(f"Taxi Data ingested successfully: {len(df_taxi)} rows.")


if __name__ == '__main__':
    main()
