from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def get_logs(user_id=None):
    conn = psycopg2.connect("dbname=test user=postgres password=yourpassword")
    cur = conn.cursor()
    if user_id:
        cur.execute("SELECT * FROM logs WHERE user_id = %s", (user_id,))
    else:
        cur.execute("SELECT * FROM logs")
    logs = cur.fetchall()
    cur.close()
    conn.close()
    return logs

@app.route('/logs', methods=['GET'])
def logs():
    return jsonify(get_logs())

@app.route('/logs/<int:user_id>', methods=['GET'])
def logs_by_user(user_id):
    return jsonify(get_logs(user_id))

if __name__ == '__main__':
    app.run(debug=True)