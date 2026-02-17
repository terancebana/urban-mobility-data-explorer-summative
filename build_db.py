import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Float, Text, BigInteger
import io
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv("server/.env")

# Connection to the postgres db
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

parquet_file = "./cleaned_integrated_data.parquet"
print("Starting database migration")
print(f"Commencing read of {parquet_file}")
df = pd.read_parquet(parquet_file).head(1000000) # df = dataframe

df['tpep_pickup_datetime'] = df['tpep_pickup_datetime'].astype(str)
df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].astype(str)

print(f"Prepared {len(df)} rows.")

# dtypes for SQLAlchemy
dtype_mapping = {
    'VendorID': BigInteger,
    'tpep_pickup_datetime': Text,
    'tpep_dropoff_datetime': Text,
    'passenger_count': Integer,
    'trip_distance': Float,
    'RatecodeID': Integer,
    'store_and_fwd_flag': Text,
    'PULocationID': Integer,
    'DOLocationID': Integer,
    'payment_type': Integer,
    'fare_amount': Float,
    'extra': Float,
    'mta_tax': Float,
    'tip_amount': Float,
    'tolls_amount': Float,
    'improvement_surcharge': Float,
    'total_amount': Float,
    'congestion_surcharge': Float,
    'pickup_borough': Text,
    'pickup_zone': Text,
    'dropoff_borough': Text,
    'dropoff_zone': Text,
    'duration_hours': Float,
    'avg_speed_kmh': Float,
    'fare_per_mile': Float,
    'pickup_hour': Integer
}

engine = create_engine(DATABASE_URL)

df.head(0).to_sql("trips", engine, if_exists="replace", index=False, dtype=dtype_mapping)
print("Table namely 'Trips' is created or replaced with the schema.")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Loading the CSV buffer
print("Conversion of dataframe to CSV buffer")
csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False, header=False)
csv_buffer.seek(0)

print("copying data to database using COPY command")
try:
    cur.copy_expert("COPY trips FROM STDIN WITH (FORMAT CSV)", csv_buffer)
    conn.commit()
    print("Data upload completed successfully.")
except Exception as e:
    print(f"Error while uploading data: {e}")
    exit(1)

# Implementation of indexing for efficient queries
print("Creating INdex for performace")
try:
    cur.execute("CREATE INDEX IF NOT EXISTS idx_pickup_borough ON trips (pickup_borough)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_pickup_hour ON trips (pickup_hour)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_fare ON trips(fare_amount)")
    conn.commit() # commit = save
    print("Indexes got created successfully.")
except Exception as e:
    print(f"Error while creating indexes: {e}")

cur.close()
conn.close()
print("Database MigrationCompleted successfully")