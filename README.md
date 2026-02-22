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

### Urban mobility link

<a href="https://docs.google.com/document/d/1yJHmQs-b9ZgbPX3cwFdPVxoIYPGXpre9IfUEcA0bdxk/edit?usp=sharing">Urban mobility Document on GOOGLE DRIVE</a>

### TEAM TASK SHEET LINK

<a href="https://docs.google.com/spreadsheets/d/1ppa5uTeBi0YLsOZ3MW28Z7nH5G65H0UAycVMeB2_LDg/edit?usp=sharing">TEAM 10'S Task Sheet</a>

### Video link

<a href="">TEAM 10</a>

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
git clone <repo_url>
cd urban-mobility
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
Database-only Validation
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
    "id": "76662021700",
    "type": "Transfer Received",
    "amount": 2000.0,
    "sender": "Jane Smith",
    "receiver": "Mobile Money User",
    "timestamp": "10 May 2024 4:30:58 PM"
  }

  {
    "id": "76662021702",
    "type": "Payment Sent",
    "amount": 1500.0,
    "sender": "John Smith",
    "receiver": "Mobile Money User",
    "timestamp": "13 May 2024 6:00:00 PM"
  }
]
```

2. **List top fare**
   To list top fare we use the following Endpoint:

- **Endpoint**: `GET /api/top_fares`
- **Success Response**: `200 OK`
- **Error Response**: `404 Not Found`

### Error Codes

| Code | Meaning      | Desc                                                                  |
| ---- | ------------ | --------------------------------------------------------------------- |
| 200  | OK           | Request has succeeded                                                 |
| 201  | Created      | Resource was added successfuly                                        |
| 400  | Bad Request  | Invalid JSON body or a field is missing                               |
| 401  | Unauthorized | Missing auth credentials                                              |
| 404  | Not Found    | The requested endpoint is not present or transaction ID doesnot exist |

### Security and Accuracy logic

1. **Authorization Guard**: every req made is supposed to pass through the `authenticate()` check before being allowed to reach the route logic
2. **INput Validation**: `POST` and `PUT` methods verifies that the req body is valid JSON
3. **Data integrity**: Transactions ID must be unique, if an existing ID is found it should return `404 Bad Request` when a `Post ` request is passed