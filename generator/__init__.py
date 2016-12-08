from flask import Flask, render_template, json, request
app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('generator.html')

@app.route(('/json_to_query/'), methods=['POST'])
def json_to_query():
	feedback = json.dumps(request.get_json())
	return json.jsonify(feedback=feedback)

if __name__ == "__main__":
	app.run()