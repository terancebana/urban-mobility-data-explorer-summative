import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("server/.env")

url = os.getenv("DATABASE_URL")
print(f"Testing connection to: {url}")

try:
    conn = psycopg2.connect(url)
    print("Connection successful!")
    conn.close()
except psycopg2.OperationalError as e:
    print(f"Connection failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
