from flask import Flask
from flask import request, jsonify
from os import path
import sqlite3
import random
import datetime
from pathlib import Path

# current script name
script_name = path.basename(__file__)
# Init server
app = Flask(__name__)
# path to database in use. pathlib library is used to generalize path for both osx and windows
# database = r"..\NemID_ESB\nem_id_database.sqlite"
# database = r"../NemID_ESB/nem_id_database.sqlite"
database = Path("../NemID_ESB/nem_id_database.sqlite")


# establishing connection to the database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn


# check if the user exist (is registered) in the database by specifying nemId, password, and current open connection
# return user's id if the user was found
def check_if_user_exits(conn, password, nemdId):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE Password=? AND NemID=?", (password, nemdId))
        # fetch the user if found
        row = cursor.fetchone()
        if row is None:
            raise ValueError('No user found')
        else:
            # row[0] will return ID of the user since it is a first element in the row
            return row[0]
    except Exception as e:
        print(e)


def store_in_database(conn, user_id, auth_code):
    try:
        timestamp = datetime.datetime.now().timestamp()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO auth_log(UserId, Code, Timestamp) VALUES (?,?,?)', (user_id, auth_code, timestamp))
        conn.commit()
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
            user_id = check_if_user_exits(conn, password, nemId)
            if user_id is not None:
                # generate nemID auth code
                generated_code = random.randint(100000, 999999)
                # store authentication log in the database
                store_in_database(conn, user_id, generated_code)
                # return generated code
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
