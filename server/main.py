import os
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    # Use absolute path relative to this script for robustness
    try:
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        return conn
    except Exceptions as e:
        raise ConnectionError(f"The connection to database failed: {e}")

@app.route('/api/trips', methods=['GET'])
def get_trips():
    # Capture options to filter from the request
    borough = request.args.get('borough')
    try:
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return jsonify({"error": "Limit and offset must be integers"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM trips"
        params = []
        
        if borough:
            query += " WHERE pickup_borough = %s"
            params.append(borough)
        
        query += " LIMIT %s OFFSET %s"
        params.append(limit)
        params.append(offset)
        
        cur.execute(query, params)
        trips = cur.fetchall()
        conn.close()
        
        fares_per_km = []
        for trip in trips:
            if trip.get('fare_amount') is not None and trip.get('trip_distance') and trip['trip_distance'] > 0:
                fare_per_km = trip['fare_amount'] / trip['trip_distance']
                fares_per_km.append(fare_per_km)

        if fares_per_km:
            mean = sum(fares_per_km) / len(fares_per_km)
            variance = sum((x - mean) ** 2 for x in fares_per_km) / len(fares_per_km)
            std_dev = variance ** 0.5
 
            for trip in trips:
                if trip.get('fare_amount') is not None and trip.get('trip_distance') and trip['trip_distance'] > 0:
                    fare_per_km = trip['fare_amount'] / trip['trip_distance']
                    trip['fare_per_km'] = fare_per_km
                    trip['is_overpaying'] = fare_per_km > mean + 2 * std_dev
                else:
                    trip['fare_per_km'] = None
                    trip['is_overpaying'] = False                

        return jsonify([dict(row) for row in trips])
    except Exception as e:
        return jsonify({"error" : f"Failed to fetch trips: {e}"}), 500

# PLACEHOLDER FOR VUX


if __name__ == "__main__":
    app.run(debug=True, port=5000)
