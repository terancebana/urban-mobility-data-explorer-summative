import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    # Use absolute path relative to this script for robustness
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'assets', 'urban_mobility.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # Allows us to access columns by name
    return conn

@app.route('/api/trips', methods=['GET'])
def get_trips():
    # Capture options to filter from the request
    borough = request.args.get('borough')
    limit = request.args.get('limit', 100)

    try:
        limit = int(limit)
    except ValueError:
        limit = 100

    conn = get_db_connection()
    query = "SELECT * FROM trips"
    params = []

    if borough:
        query += " WHERE pickup_borough = ?"
        params.append(borough)

    query += " LIMIT ?"
    params.append(limit)

    try:
        trips = conn.execute(query, params).fetchall()
        return jsonify([dict(row) for row in trips])
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# PLACEHOLDER FOR VUX


if __name__ == "__main__":
    app.run(debug=True, port=5000)