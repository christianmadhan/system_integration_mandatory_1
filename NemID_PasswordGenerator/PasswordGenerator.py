from flask import Flask
from flask import request, jsonify
from os import path
import random

# current script name
script_name = path.basename(__file__)

# Init server
app = Flask(__name__)


# When receiving POST request, create password for nemId
@app.route('/generate-password-nemID', methods=['POST'])
def generate_password_nemId():
    try:
        cpr = request.json['cpr']
        nemId = request.json['nemId']
        password = generate_password(cpr, nemId)
        return jsonify({"nemIdPassword": password}), 200

    except Exception as e:
        print(
            f"******* Error in {script_name} when generating password for nemId *******")
        print(f"Error: {e}")
        return jsonify("Cannot generate password!"), 500


def generate_password(cpr, nemId):
    last_two_digits_cpr = cpr[-2:]
    first_two_digits_nemId = nemId[:2]
    return f'{first_two_digits_nemId}{last_two_digits_cpr}'


# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8089)
