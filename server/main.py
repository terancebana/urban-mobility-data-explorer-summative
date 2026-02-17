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
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    return conn

@app.route('/api/trips', methods=['GET'])
def get_trips():
    # Capture options to filter from the request
    borough = request.args.get('borough')
    limit = request.args.get('limit', 100)
    offset = request.args.get('offset', 0)

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM trips"
    params = []

    if borough:
        query += " WHERE pickup_borough = ?"
        params.append(borough)

    query += " LIMIT ?"
    params.append(limit)
    params.append(offset)

    cur.execute(query, params)
    trips = cur.fetchall()
    conn.close()

    return jsonify([dict(row) for row in trips])

# PLACEHOLDER FOR VUX


if __name__ == "__main__":
    app.run(debug=True, port=5000)