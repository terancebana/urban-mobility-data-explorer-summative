import pandas as pd
import logging
from pathlib import Path

def setup_logging():
    Path('logs').mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', filename='logs/cleaning_log.txt', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

def process_chunk(df, zones):
    mask = (
        (df['fare_amount'] >= 0) &
        (df['trip_distance'] >= 0) &
        (df['passenger_count'].between(1, 9)) &
        (df['tpep_dropoff_datetime'] > df['tpep_pickup_datetime'])
    )
    df = df[mask].copy()

    zone_map = zones.set_index('LocationID')['Zone']
    df['pickup_zone'] = df['PULocationID'].map(zone_map)
    df['dropoff_zone'] = df['DOLocationID'].map(zone_map)

    df['trip_duration_min'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
    df['trip_speed_mph'] = (df['trip_distance'] / (df['trip_duration_min'] / 60)).fillna(0)
    df['fare_per_mile'] = (df['fare_amount'] / df['trip_distance']).replace([float('inf'), -float('inf')], 0).fillna(0)

    return df

def process_data():
    setup_logging()
    DATA_DIR = Path('data')
    TRIP_FILE = DATA_DIR / 'yellow_tripdata_2019-01.csv'
    ZONE_FILE = DATA_DIR / 'taxi_zone_lookup.csv'

    if not TRIP_FILE.exists() or not ZONE_FILE.exists():
        logging.error("Data files not found.")
        return

    logging.info("Loading zones...")
    zones = pd.read_csv(ZONE_FILE)

    chunk_size = 500000
    processed_chunks = []

    logging.info(f"Processing {TRIP_FILE} in chunks of {chunk_size}...")

    # Read CSV in chunks
    with pd.read_csv(TRIP_FILE, parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'], chunksize=chunk_size) as reader:
        for i, chunk in enumerate(reader):
            logging.info(f"Processing chunk {i+1}...")
            processed_chunk = process_chunk(chunk, zones)
            processed_chunks.append(processed_chunk)

    logging.info("Concatenating chunks...")
    final_df = pd.concat(processed_chunks)

    output_file = 'cleaned_integrated_data.parquet'
    logging.info(f"Saving {len(final_df)} records to {output_file}...")
    final_df.to_parquet(output_file, index=False)
    logging.info("Done.")

if __name__ == "__main__":
    process_data()
