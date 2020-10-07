from flask import Flask
from flask import request, jsonify
from os import path
import random

# current script name
script_name = path.basename(__file__)

# Init server
app = Flask(__name__)


# When receiving POST request, create nemId for the user
@app.route('/generate-nemId', methods=['POST'])
def generate_nemId():
	try:
		cpr = request.json['cpr']
		generate_nemId_number(cpr)
		return jsonify({"nemId": "44445"}), 201

	except Exception as e:
		print(f"******* Error in {script_name} when generating nemId *******")
		print(f"Error: {e}")
		return jsonify("Cannot create nemId!"), 500


def generate_nemId_number(cpr):
	last_four_digits = cpr[-4:]
	random_five_digits = random.randint(10000, 99999)
	return f'{random_five_digits}-{last_four_digits}'


# Run app
if __name__ == '__main__':
	app.run(debug=True)
