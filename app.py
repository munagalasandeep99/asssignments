from flask import Flask, jsonify
import psycopg2
from psycopg2 import OperationalError
import os

app = Flask(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="appdb",
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
        return conn
    except OperationalError as e:
        return None

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/db-test')
def db_test():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"status": "error", "message": "Database connection failed...."}), 500
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        return jsonify({"status": "success", "message": "Database connection successful"})
    except OperationalError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)

