from flask import Flask, jsonify, request
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Obtenir la valeur de GOOGLE_API_KEY
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configuration de genai avec la clé API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class MyGenerativeModel:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')

    def generateContent(self, input_text):
        return self.model.generate_content(input_text)

app = Flask(__name__)

# Créer une instance du modèle
my_model = MyGenerativeModel()

@app.route('/')
def index():
    return jsonify({"message": "hello"})

@app.route('/generate', methods=['POST'])
def generate_query():
    
    if request.method == 'POST':
        input_text = request.json.get('input_text')
        print(input_text)
        if input_text:
            # Générer le contenu
            generated_content = model.generate_content(input_text)
            # Renvoyer la réponse au format JSON
            
            sql_query = generated_content.text.split('```sql\n')[1].split('\n```')[0]

            return jsonify({'generated_query': sql_query})
        else:
            return jsonify({"error": "input_text is missing"}), 400
    else:
        return jsonify({"error": "Method not allowed"}), 405
    



if __name__ == '__main__':
    app.run(debug=True)
