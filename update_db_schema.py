import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv("server/.env")
DATABASE_URL = os.getenv("DATABASE_URL")

def update_schema():
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()


    print("Creating taxi_zones table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS taxi_zones (
            "LocationID" integer PRIMARY KEY,
            "Borough" text,
            "Zone" text,
            "service_zone" text
        );
    """)

    csv_path = "data/taxi_zone_lookup.csv"
    if os.path.exists(csv_path):
        print(f"Populating taxi_zones from {csv_path}...")
        df_zones = pd.read_csv(csv_path)


        from sqlalchemy.types import Integer, Text
        engine = create_engine(DATABASE_URL)


        df_zones.to_sql('taxi_zones', engine, if_exists='replace', index=False, dtype={
            "LocationID": Integer,
            "Borough": Text,
            "Zone": Text,
            "service_zone": Text
        })


        print("Adding Primary Key to taxi_zones...")
        cur.execute('ALTER TABLE taxi_zones ADD PRIMARY KEY ("LocationID");')
    else:
        print(f"Warning: {csv_path} not found. taxi_zones table created but empty.")


    print("Creating trips_normalized table...")

    cur.execute("DROP TABLE IF EXISTS trips_normalized;")




    cur.execute("""
        CREATE TABLE trips_normalized AS
        SELECT
            "VendorID",
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "passenger_count",
            "trip_distance",
            "RatecodeID",
            "store_and_fwd_flag",
            "PULocationID",
            "DOLocationID",
            "payment_type",
            "fare_amount",
            "extra",
            "mta_tax",
            "tip_amount",
            "tolls_amount",
            "improvement_surcharge",
            "total_amount",
            "congestion_surcharge",
            "trip_duration_min" / 60.0 AS "duration_hours",
            "trip_speed_mph" * 1.60934 AS "avg_speed_kmh",
            "fare_per_mile",
            "pickup_hour"
        FROM trips;
    """)
    print(f"trips_normalized populated from trips. Row count: {cur.rowcount}")


    print("Adding constraints...")
    try:
        cur.execute('ALTER TABLE trips_normalized ADD FOREIGN KEY ("PULocationID") REFERENCES taxi_zones("LocationID");')
        print("FK PULocationID added.")
    except Exception as e:
        print(f"Error adding FK PULocationID: {e}")

    try:
        cur.execute('ALTER TABLE trips_normalized ADD FOREIGN KEY ("DOLocationID") REFERENCES taxi_zones("LocationID");')
        print("FK DOLocationID added.")
    except Exception as e:
        print(f"Error adding FK DOLocationID: {e}")

    cur.close()
    conn.close()
    print("Schema update completed.")

if __name__ == "__main__":
    from sqlalchemy import text
    update_schema()
