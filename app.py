from flask import Flask, jsonify, request
from flask_cors import CORS
from executionqeury import executionquery
from query_sql_generator import generate_sql_query
from explanation_generator import generate_explanation
from sql_validator import sql_validator
from Oracle_fonction import connect_to_oracle, get_execution_plan , getTables
app = Flask(__name__)
CORS(app)

@app.route('/connect_test')
def test_db_connection():
    try:
        connection = connect_to_oracle()
        connection.close()

        return jsonify({'message': 'Connexion réussie à la base de données Oracle'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/tables')
def get_tables():
    try:
         # Récupération des résultats
        tables = getTables()
        return jsonify({'tables': tables})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_query():
    if request.method == 'POST':
        input_text = request.json.get('input_text')
        if input_text:
            sql_query = generate_sql_query(input_text)
            explanation = generate_explanation(sql_query)
            return jsonify({'generated_query': sql_query, 'explanation': explanation})
        else:
            return jsonify({"error": "input_text is missing"}), 400
    else:
        return jsonify({"error": "Method not allowed"}), 405

@app.route('/analyze-sql', methods=['POST'])
def analyze_sql():
    data = request.json
    if 'query' not in data:
        return jsonify({"status": "error", "message": "Query is required"}), 400
    query = data['query']
    result = sql_validator(query)
    return jsonify(result)

@app.route('/execution-plan', methods=['POST'])
def execution_plan():
    data = request.json
    if 'query' not in data:
        return jsonify({"error": "Query is required"}), 400
    query = data['query']
    try:
        plan = get_execution_plan(query)
        return jsonify({"execution_plan": plan})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/execute-query', methods=['POST'])
def execute_query():
    data = request.json
    if 'query' not in data:
        return jsonify({"error": "SQL query is required"}), 400
    sql_query = data['query']
    try:
        result = executionquery(sql_query)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return jsonify({"message": "hello"})


if __name__ == '__main__':
    app.run(debug=True)
