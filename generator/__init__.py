from flask import Flask, render_template, json, request
app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('generator.html')

def convert_to_transmart(genericquery):

		transmartquery = []

		for genericquerypart in genericquery:
			subtransmartquery = {}
			condition = genericquerypart.get('condition')

			if condition is not None:
				subgenericquery = genericquerypart['rules']
				childtransmartquery, lengthchildren = convert_to_transmart(subgenericquery)
				
				if lengthchildren == 1:
					subtransmartquery = childtransmartquery[0]
				else:
					subtransmartquery['type'] = "Combination"
					subtransmartquery['operator'] = condition.lower()
					subtransmartquery['args'] = childtransmartquery

				if genericquerypart.get('not') == True:
					notsubtransmartquery = {}
					notsubtransmartquery['type'] = 'Negation'
					notsubtransmartquery['arg'] = subtransmartquery
					subtransmartquery = notsubtransmartquery

			elif genericquerypart['field'] == 'patientSetId':
				subtransmartquery['type'] = 'PatientSetConstraint'
				subtransmartquery['patientSetId'] = genericquerypart['value']
				
			elif genericquerypart['field'] == 'patientIds':
				subtransmartquery['type'] = 'PatientSetConstraint'
				subtransmartquery['patientIds'] = genericquerypart['value']

			elif genericquerypart['field'] == 'StudyNameConstraint':
				subtransmartquery['type'] = 'StudyNameConstraint'
				subtransmartquery['studyId'] = genericquerypart['value']

			elif genericquerypart['field'] == 'ConceptConstraint':
				subtransmartquery['type'] = 'ConceptConstraint'
				subtransmartquery['path'] = genericquerypart['value']

			transmartquery += [subtransmartquery]
		
		return transmartquery, len(genericquery)

@app.route(('/json_to_query/'), methods=['POST'])
def json_to_query():
	querydata = request.get_json()
	genericquery = querydata['genericquery']

	transmartquery, lengthchildren = convert_to_transmart([genericquery])

	transmartquery = genericquery = querydata['url'] + '/v2/' + querydata['entities'] + '?constraint=' + json.dumps(transmartquery[0])
	return json.jsonify(transmartquery=transmartquery)

if __name__ == "__main__":
	app.run()