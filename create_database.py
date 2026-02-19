import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv("server/.env")

url = os.getenv("DATABASE_URL")

# We need to connect to the default 'postgres' database to create a new one.
# Replaces the database name in the connection string.
if "/urban_mobility" in url:
    postgres_url = url.replace("/urban_mobility", "/postgres")
else:
    # Fallback/Debug
    print(f"Could not parse URL to switch to 'postgres' db: {url}")
    exit(1)

print(f"Connecting to 'postgres' database to create 'urban_mobility'...")

try:
    conn = psycopg2.connect(postgres_url)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Check if database already exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'urban_mobility'")
    exists = cur.fetchone()

    if not exists:
        print("Creating database 'urban_mobility'...")
        cur.execute("CREATE DATABASE urban_mobility")
        print("Database 'urban_mobility' created successfully!")
    else:
        print("Database already exists.")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Error creating database: {e}")
    print("Please ensure your user has CREATEDB privileges.")
