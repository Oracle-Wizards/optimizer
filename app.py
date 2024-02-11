from flask import Flask, jsonify, request
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')



app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return jsonify({"message": "hello"})

@app.route('/generate', methods=['POST'])
def generate_query():
    
    if request.method == 'POST':
        INPUT = " Gener une requete sql optimiser oracle  pour :" + request.json.get('input_text') + " ,sous la forme [Requête SQL]"
        input_text = request.json.get('input_text')
        print(request)
        if input_text:
            generated_content = model.generate_content(INPUT)
            
            sql_query = generated_content.text.split('```sql\n')[1].split('\n```')[0]
            
            generated_text = "donner un petite explication pour :" + sql_query #+ " ,sous la forme [Explication]"
        
            Explication  = model.generate_content(generated_text)

            return jsonify({'generated_query': sql_query ,'explanation': Explication.text})
        else:
            return jsonify({"error": "input_text is missing"}), 400
    else:
        return jsonify({"error": "Method not allowed"}), 405
    



if __name__ == '__main__':
    app.run(debug=True)
