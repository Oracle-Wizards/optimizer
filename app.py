from flask import Flask, jsonify, request
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS
from query_sql_generator import generate_sql_query
from explanation_generator import generate_explanation
from sql_validator import sql_validator
app = Flask(__name__)
CORS(app)



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

if __name__ == '__main__':
    app.run(debug=True)
