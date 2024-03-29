from flask import Flask, jsonify, request
from flask_cors import CORS
from executionqeury import executionquery
from query_sql_generator import generate_sql_query
from explanation_generator import generate_explanation
from sql_validator import sql_validator ,sql_validator1 ,analyze_sql_query
from Oracle_fonction import connect_to_oracle, get_execution_plan , getTables , transform_execution_plan
from llama_api_optimization import optimiser_requete
from query_sql_generator import generate_sql_query , extract_optimized_sql_query
import json
from datetime import datetime


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
    
    
@app.route('/analyze_sql', methods=['POST'])
def analyze_sql():
    data = request.json
    if 'query' not in data:
        return jsonify({"status": "error", "message": "Query is required"}), 400
    query = data['query']
    result = sql_validator(query)

    if result == {"status": "success", "message": "Query is valid"} :
        # text = optimiser_requete(query)
        # optimized_query  = extract_optimized_sql_query(text)
        # print("optimized query: ", optimized_query)
        # return jsonify({"optimized_query": optimized_query})
        return jsonify({"status": "success", "message": "Query is valid"})
    else:
        return jsonify({"status": "error", "message": "Query is invalid"}), 500
    
# @app.route('/optimise-query', methods=['POST'])
# def optimise_query():
#     data = request.json
#     if 'query' not in data:
#         return jsonify({"status": "error", "message": "Query is required"}), 400
#     query = data['query']
#     text = optimiser_requete(query)
#     optimized_query  = extract_optimized_sql_query(text)
#     print("optimized query: ", optimized_query)
#     return jsonify({"optimized_query": optimized_query})
@app.route('/api/validation', methods=['POST'])
def handle_query():
    try:
        # Extract the SQL query from the request JSON data
        data = request.get_json()
        query = data['query']

        # Validate the SQL query
        validation_result = sql_validator1(query)

        # If validation succeeds, analyze the SQL query
        analysis_result = analyze_sql_query(query)

        # Respond with the analysis result
        return jsonify(analysis_result), 200
    except Exception as e:
        # Handle any errors that occur during the processing of the request
        print('Error processing query:', str(e))
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/optimise_query', methods=['POST'])
def optimise_query():
    data = request.json
    if 'query' not in data:
        return jsonify({"status": "error", "message": "Query is required"}), 400
    query = data['query']
    text = optimiser_requete(query)
    optimized_query = extract_optimized_sql_query(text)
    # Encode the optimized query explicitly before printing
    print("optimized query: ", optimized_query.encode('utf-8', errors='ignore'))
    return jsonify({"optimized_query": optimized_query})


@app.route('/execution-plan', methods=['POST'])
def execution_plan():
    data = request.json
    if 'query' not in data:
        return jsonify({"error": "Query is required"}), 400
    query = data['query']
    try:
        plan = get_execution_plan(query)
        transformed_plan = transform_execution_plan(plan)
        return jsonify({"execution_plan": transformed_plan})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
# @app.route('/execute-query', methods=['POST'])
# def execute_query():
#     data = request.json
#     if 'query' not in data:
#         return jsonify({"error":  "SQL query is required"}), 400
#     sql_query = data['query']
#     try:
#         result = executionquery(sql_query)
#         response_data = {"optimized_query": result}
#         json_response = json.dumps(response_data)
#         return json_response
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@app.route('/execute-query', methods=['POST'])
def execute_query():
    data = request.json
    if 'query' not in data:
        return jsonify({"error":  "SQL query is required"}), 400
    sql_query = data['query']
    try:
        result = executionquery(sql_query)
        # Check if result is a datetime object
        if isinstance(result, datetime):
            # Convert datetime object to string
            result_str = result.isoformat()
            response_data = {"optimized_query": result_str}
        else:
            response_data = {"optimized_query": result}
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route('/optimize', methods=['POST'])  # Define a new route
# def optimize_query():
#     data = request.json
#     if 'query' not in data:
#         return jsonify({"error": "Query is required"}), 400
#     query = data['query']
#     try:
#         optimized_query = optimiser_requete(query)
#         return jsonify({"optimized_query": optimized_query})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return jsonify({"message": "hello"})



if __name__ == '__main__':
    app.run(debug=True)