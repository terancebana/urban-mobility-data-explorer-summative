from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    return conn

@app.route('/api/trips', methods=['GET'])
def get_trips():
    borough = request.args.get('borough')
    limit = request.args.get('limit', 100)
    offset = request.args.get('offset', 0)

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
    trips = [dict(row) for row in cur.fetchall()]
    conn.close()

    fares_per_mile = []
    for trip in trips:
        dist = trip.get('trip_distance', 0)
        fare = trip.get('fare_amount', 0)

        if dist and dist > 0:
            fpm = fare / dist
            trip['fare_per_mile'] = round(fpm, 2)
            fares_per_mile.append(fpm)
        else:
            trip['fare_per_mile'] = 0

    if fares_per_mile:
        mean = sum(fares_per_mile) / len(fares_per_mile)
        variance = sum((x - mean) ** 2 for x in fares_per_mile) / len(fares_per_mile)
        std_dev = variance ** 0.5

        for trip in trips:
            fpm = trip.get('fare_per_mile', 0)
            trip['is_overpaying'] = fpm > (mean + 2 * std_dev)
    else:
        for trip in trips:
            trip['is_overpaying'] = False

    return jsonify(trips)

@app.route('/api/top_fares', methods=['GET'])
def get_top_fare():

    borough = request.args.get('borough', 'Manhattan')
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT pickup_borough, dropoff_borough, fare_amount FROM trips WHERE pickup_borough = %s LIMIT 50", (borough,))
    raw_trips = cur.fetchall()
    conn.close()

    trip_data = [dict(row) for row in raw_trips]

    sorted_trips = manual_sort_by_fare(trip_data)

    return jsonify(sorted_trips[:50])

def manual_sort_by_fare(trip_list):
    n = len(trip_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if trip_list[j]['fare_amount'] < trip_list[j + 1]['fare_amount']:
                trip_list[j], trip_list[j + 1] = trip_list[j + 1], trip_list[j]
    return trip_list




if __name__ == "__main__":
    app.run(debug=True, port=5001)