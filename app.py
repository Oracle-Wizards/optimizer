from flask import Flask, jsonify, request
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS
from query_sql_generator import generate_sql_query
from explanation_generator import generate_explanation
from sql_validator import sql_validator
import oracledb

app = Flask(__name__)
CORS(app)

# Configuration de la base de données Oracle
oracle_connection_string = 'CO/BETTER_CO@better-sql.francecentral.cloudapp.azure.com/FREE'

# Fonction pour se connecter à la base de données Oracle
def connect_to_oracle():
    connection = oracledb.connect(oracle_connection_string)
    return connection

# Route de test pour vérifier la connexion à la base de données
@app.route('/connect_test')
def test_db_connection():
    try:
        connection = connect_to_oracle()
        connection.close()

        return jsonify({'message': 'Connexion réussie à la base de données Oracle'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    

# Route pour obtenir la liste des tables de la base de données
@app.route('/tables')
def get_tables():
    try:
        connection = connect_to_oracle()
        cursor = connection.cursor()

        # Exécution de la requête SQL pour récupérer la liste des tables
        cursor.execute("SELECT table_name FROM user_tables")

        # Récupération des résultats
        tables = [row[0] for row in cursor.fetchall()]

        # Fermeture du curseur et de la connexion
        cursor.close()
        connection.close()

        return jsonify({'tables': tables})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return jsonify({"message": "hello"})

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



# Fonction pour obtenir le plan d'exécution d'une requête SQL
def get_execution_plan(query):
    connection = connect_to_oracle()
    cursor = connection.cursor()
    cursor.execute("EXPLAIN PLAN FOR " + query)
    cursor.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY)")
    plan = cursor.fetchall()
    cursor.close()
    connection.close()
    return plan

# Route pour obtenir le plan d'exécution d'une requête SQL
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

if __name__ == '__main__':
    app.run(debug=True)
