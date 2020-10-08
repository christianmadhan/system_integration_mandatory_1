from flask import Flask
from flask import request, jsonify
from os import path
import sqlite3
import random

# current script name
script_name = path.basename(__file__)
# Init server
app = Flask(__name__)
# path to database in use
database = r"..\NemID_ESB\nem_id_database.sqlite"


# establishing connection to the database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn


# check if the user exist (is registered) in the database by specifying nemId, password, and current open connection
def check_if_user_exits(conn, password, nemdId):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE Password=? AND NemID=?", (password, nemdId))
        # fetch the user if found
        row = cursor.fetchone()
        if row is None:
            raise ValueError('No user found')
        else:
            return True

    except Exception as e:
        print(e)


# When receiving POST request, create generate nemId 6 digit long code
@app.route('/nemid-auth', methods=['POST'])
def generate_nemId():
    try:
        password = request.json['nemIdCode']
        nemId = request.json['nemId']

        conn = create_connection(database)
        with conn:
            response = check_if_user_exits(conn, password, nemId)
            if response:
                generated_code = random.randint(100000, 999999)
                return jsonify({"generatedCode": f"{generated_code}"}), 200
            return jsonify({"authError": "forbidden access"}), 403

    except Exception as e:
        print(
            f"******* Error in {script_name} when generating nemId authentication code *******")
        print(f"Error: {e}")
        return jsonify({"server error": "cannot generate nemID authentication code"}), 500


# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
