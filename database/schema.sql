-- Schema Export for 'trips' table
-- Generated from PostgreSQL

CREATE TABLE trips (
    "VendorID" bigint,
    "tpep_pickup_datetime" text,
    "tpep_dropoff_datetime" text,
    "passenger_count" integer,
    "trip_distance" double precision,
    "RatecodeID" integer,
    "store_and_fwd_flag" text,
    "PULocationID" integer,
    "DOLocationID" integer,
    "payment_type" integer,
    "fare_amount" double precision,
    "extra" double precision,
    "mta_tax" double precision,
    "tip_amount" double precision,
    "tolls_amount" double precision,
    "improvement_surcharge" double precision,
    "total_amount" double precision,
    "congestion_surcharge" double precision,
    "pickup_zone" text,
    "dropoff_zone" text,
    "pickup_borough" text,
    "pickup_hour" integer,
    "trip_duration_min" double precision,
    "trip_speed_mph" double precision,
    "fare_per_mile" double precision
);

-- Indexes
CREATE INDEX idx_pickup_borough ON trips (pickup_borough);
CREATE INDEX idx_pickup_hour ON trips (pickup_hour);
CREATE INDEX idx_fare ON trips (fare_amount);
