# Urban Mobility Data Explorer

The Urban Mobility Data Explorer is a full-stack system that processes NYC taxi trip data from raw CSV files to a cleaned PostgreSQL database, and exposes it through a backend API and a simple frontend interface for visualizing urban mobility insights.

## Group

### Group name

Group 10

### Members of the group

- NTIVUNWA Gilbert
- MUNEZERO Bonheur Divin
- CYUZUZO BANA Terance
- NIYONKURU MITALI Tony Robert

## Links

### System Archtecture

<a href="https://lucid.app/publicSegments/view/37742e6a-fefa-48fc-9309-cebd42d04556/image.png">System Architecture</a>

### ERD Link

<a href="https://lucid.app/publicSegments/view/8dd0ebce-5f7d-4e06-a43a-998cfe5169a4/image.png">ERD DIAGRAM ON PAGE 2...</a>

### Figma Link

<a href="https://www.figma.com/design/dd9SBuqJWb62nGqrsYh6bd/EWD10?node-id=0-1&t=w7D2vp6LdwNd5xVx-1">Figma Link</a>

### Urban mobility link

<a href="https://docs.google.com/document/d/1yJHmQs-b9ZgbPX3cwFdPVxoIYPGXpre9IfUEcA0bdxk/edit?usp=sharing">Urban mobility Document on GOOGLE DRIVE</a>

### TEAM TASK SHEET LINK

<a href="https://docs.google.com/spreadsheets/d/1ppa5uTeBi0YLsOZ3MW28Z7nH5G65H0UAycVMeB2_LDg/edit?usp=sharing">TEAM 10'S Task Sheet</a>

### Video link

<a href="https://drive.google.com/file/d/1XbQ0SbA6Puw--itnpcpIzj9VECC4hG7a/view?usp=sharing">TEAM 10</a>

## Usage

This project provides a full data pipeline → database → API → frontend workflow for exploring NYC Taxi trip data.

You will be able to:

1. Download raw CSV datasets

2. Clean and transform data

3. Build a PostgreSQL database + schema

4. Serve API endpoints using a Python backend

5. Visualize data through a simple frontend
...

## Features

### Environment Setup

```
1. Clone repository

git clone https://github.com/terancebana/urban-mobility-data-explorer-summative.git

cd urban-mobility-data-explorer-summative

2. Create and activate a virtual environment

python3 -m venv venv

source venv/bin/activate     # Linux/Mac

venv\Scripts\activate        # Windows

3. Install required libraries

Check requirements.txt and run:

pip install -r requirements.txt

4. Prepare environment variables

Copy the example file:

cp .env.example .env

Inside .env, add:

PostgreSQL host

Username

Password

Database name

API secrets (if any)

```

## Dataset Setup

### Download Required Files

Download and place the following inside the project folder:

- `yellow_tripdata_2019-01.csv`

- `taxi_zone_lookup.csv`

These are required for data cleaning and database population.

## Backend Setup (Port 5001)

### Ensure PostgreSQL is Installed

Install PostgreSQL from:
https://www.postgresql.org/download/

Start PostgreSQL in the Background

Windows: Services → Start PostgreSQL

Linux:

```
sudo service postgresql start

```

### Run Data Pipeline (Full Flow Test)

This validates:

- `Data cleaning`

- `DB schema creation`

- `Data insertion`

```

python data_pipeline.py

python build_db.py

python export_schema.py

- Database-only Validation

python test_db_connection.py

python create_database.py


```
### Run the Backend Server

Keep this running for the frontend to connect:

`python server/main.py`

The backend will start on:

http://localhost:5001

### Frontend Setup (Port 5500)

This project uses Live Server (VS Code extension).

Steps:

- Open the project in VS Code

- Right-click index.html

- Select Open with Live Server

The frontend will launch on:

http://127.0.0.1:5500

You must have backend running on port 5001 for data to load.

### API ENDPOINTS

1. **List top trips**
   To list the top trips we use the following Endpoints:

- **Endpoint**: `GET /api/trips`
- **Success Response**: `200 OK`
- **Output**:

```
[
  {
    "DOLocationID": 151,
    "PULocationID": 43,
    "RatecodeID": 1,
    "VendorID": 2,
    "avg_speed_kmh": 19.856849534555714,
    "congestion_surcharge": null,
    "dropoff_borough": "Manhattan",
    "dropoff_zone": "Manhattan Valley",
    "duration_hours": 0.19694444444444445,
    "extra": 0.5,
    "fare_amount": 11.0,
    "fare_per_mile": 4.53,
    "improvement_surcharge": 0.3,
    "is_overpaying": false,
    "mta_tax": 0.5,
    "passenger_count": 3,
    "payment_type": 1,
    "pickup_borough": "Manhattan",
    "pickup_hour": 0,
    "pickup_zone": "Central Park",
    "store_and_fwd_flag": "N",
    "tip_amount": 2.46,
    "tolls_amount": 0.0,
    "total_amount": 14.76,
    "tpep_dropoff_datetime": "2019-01-01 00:42:15",
    "tpep_pickup_datetime": "2019-01-01 00:30:26",
    "trip_distance": 2.43
  }
]
```

2. **List top fare**
   To list top fare we use the following Endpoint:

- **Endpoint**: `GET /api/top_fares`
- **Success Response**: `200 OK`
- **Output**:
```
[
 {
    "dropoff_borough": "Queens",
    "fare_amount": 5.0,
    "pickup_borough": "Queens"
  },
  {
    "dropoff_borough": "Queens",
    "fare_amount": 4.5,
    "pickup_borough": "Queens"
  }
]
```

### Error Codes

| Code | Meaning      | Desc                                                                  |
| ---- | ------------ | --------------------------------------------------------------------- |
| 200  | OK           | Request has succeeded                                                 |
| 201  | Created      | Resource was added successfuly                                        |
| 400  | Bad Request  | Invalid JSON body or a field is missing                               |
| 401  | Unauthorized | Missing auth credentials                                              |
| 404  | Not Found    | The requested endpoint is not present or transaction ID doesnot exist |
