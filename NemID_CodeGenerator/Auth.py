from flask import Flask
from flask import request, jsonify
from os import path
import sqlite3
import random

# current script name
script_name = path.basename(__file__)

# Init server
app = Flask(__name__)
database = r"..\NemID_ESB\nem_id_database.sqlite"


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(conn)
    except Exception as e:
        print(e)
    return conn


def check_if_user_exits(conn, password, nemdId):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user WHERE Password=? AND NemID=?", (password, nemdId))
        row = cursor.fetchone()
        if row is None:
            raise ValueError('No user found')
        else:
            return True

    except Exception as e:
        print(e)

# When receiving POST request, create nemId for the user


@app.route('/nemid-auth', methods=['POST'])
def generate_nemId():
    try:
        password = request.json['nemIdCode']
        nemId = request.json['nemId']

        conn = create_connection(database)
        if(conn):
            response = check_if_user_exits(conn, password, nemId)
            if(response):
                generatedCode = random.randint(100000, 999999)
                return jsonify({"generatedCode": f"{generatedCode}"}), 200
            return jsonify({"authError": "forbidden access"}), 403
        else:
            return jsonify({"authError": "Connection not established"}), 500

    except Exception as e:
        print(
            f"******* Error in {script_name} when generating nemid auth code *******")
        print(f"Error: {e}")
        return jsonify("Cannot create nemid auth code!"), 500


# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
