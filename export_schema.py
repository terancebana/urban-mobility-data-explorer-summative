import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv("server/.env")

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

try:
    engine = create_engine(DATABASE_URL)

    print("Fetching table structure for 'trips' from information_schema...")

    query = """
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'trips'
    ORDER BY ordinal_position;
    """

    columns_df = pd.read_sql(query, engine)

    create_table_stmt = "CREATE TABLE trips (\n"
    column_defs = []

    for _, row in columns_df.iterrows():
        col_name = f'"{row["column_name"]}"'
        col_type = row['data_type']
        column_defs.append(f"    {col_name} {col_type}")

    create_table_stmt += ",\n".join(column_defs)
    create_table_stmt += "\n);"

    table_schema = create_table_stmt

    indexes = [
        "CREATE INDEX idx_pickup_borough ON trips (pickup_borough);",
        "CREATE INDEX idx_pickup_hour ON trips (pickup_hour);",
        "CREATE INDEX idx_fare ON trips (fare_amount);"
    ]

    output_dir = 'database'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = f'{output_dir}/schema.sql'

    with open(output_file, 'w') as f:
        f.write("-- Schema Export for 'trips' table\n")
        f.write("-- Generated from PostgreSQL\n\n")

        f.write(table_schema)
        if not table_schema.strip().endswith(';'):
            f.write(";")
        f.write("\n\n")

        f.write("-- Indexes\n")
        for idx in indexes:
            f.write(f"{idx}\n")

    print(f"Schema successfully exported to {output_file}")

except Exception as e:
    print(f"Error exporting schema: {e}")
