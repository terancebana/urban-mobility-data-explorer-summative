import sqlite3
import pandas as pd

# Connection to the sqlite db
conn = sqlite3.connect('./assets/urban_mobility.db')

parquet_file = "./cleaned_integrated_data.parquet"
print("Starting database migration")
df = pd.read_parquet(parquet_file) # df = dataframe

df['tpep_pickup_datetime'] = df['tpep_pickup_datetime'].astype(str)
df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].astype(str)

df.to_sql("trips", conn, if_exists="replace", index=False)

# Implementation of indexing for efficient queries
print("Creating INdex for performace")
cursor = conn.cursor() #cursor = pointer
cursor.execute("CREATE INDEX idx_pickup_borough ON trips (pickup_borough)")
cursor.execute("CREATE INDEX idx_pickup_hour ON trips (pickup_hour)")
cursor.execute("CREATE INDEX idx_fare ON trips(fare_amount)")
conn.commit() # commit = save

# Export the schema for the deliverable 'database/schema.sql'
with open('database/schema.sql', 'w') as f:
    for line in conn.iterdump(): # iterdump = export
        f.write(f"{line}\n")

print("Database and schema.sql generated successfully")
conn.close()