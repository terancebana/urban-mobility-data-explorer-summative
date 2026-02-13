import pandas as pd
import logging
from pathlib import Path

def setup_logging():
    Path('logs').mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', filename='logs/cleaning_log.txt', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

def process_data():
    setup_logging()
    DATA_DIR = Path('data')
    TRIP_FILE = DATA_DIR / 'yellow_tripdata_2019-01.csv'
    ZONE_FILE = DATA_DIR / 'taxi_zone_lookup.csv'

    if not TRIP_FILE.exists() or not ZONE_FILE.exists():
        logging.error("Data files not found.")
        return

    logging.info("Loading data...")
    df = pd.read_csv(TRIP_FILE, parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'])
    zones = pd.read_csv(ZONE_FILE)

    initial_len = len(df)
    logging.info(f"Loaded {initial_len} records.")

    mask = (
        (df['fare_amount'] >= 0) &
        (df['trip_distance'] >= 0) &
        (df['passenger_count'].between(1, 9)) &
        (df['tpep_dropoff_datetime'] > df['tpep_pickup_datetime'])
    )
    df = df[mask].copy()
    logging.info(f"Removed {initial_len - len(df)} invalid records.")

    logging.info("Integrating zones...")
    zone_map = zones.set_index('LocationID')['Zone']
    borough_map = zones.set_index('LocationID')['Borough']

    df['pickup_zone'] = df['PULocationID'].map(zone_map)
    df['dropoff_zone'] = df['DOLocationID'].map(zone_map)
    df['pickup_borough'] = df['PULocationID'].map(borough_map)

    # Extract hour for indexing
    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour

    logging.info("Engineering features...")
    df['trip_duration_min'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60

    df['trip_speed_mph'] = (df['trip_distance'] / (df['trip_duration_min'] / 60)).fillna(0)

    df['fare_per_mile'] = (df['fare_amount'] / df['trip_distance']).replace([float('inf'), -float('inf')], 0).fillna(0)

    output_file = 'cleaned_integrated_data.parquet'
    logging.info(f"Saving {len(df)} records to {output_file}...")
    df.to_parquet(output_file, index=False)
    logging.info("Done.")

if __name__ == "__main__":
    Path('logs').mkdir(exist_ok=True)
    process_data()
