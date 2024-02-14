from openai import OpenAI
import os
from dotenv import load_dotenv
from flask import jsonify, request

load_dotenv()

client = OpenAI(
    api_key=os.getenv('llama_key'),
    base_url="https://api.llama-api.com"
)

# Fonction pour optimiser la requête SQL
def optimiser_requete(requete_sql):
    response = client.chat.completions.create(
        model="llama-13b-chat",
        messages=[
            {"role": "system", "content": "Optimize the following SQL query in the following form '''sql : " + requete_sql + "''' end :"}
        ]
    )
    optimized_query = response.choices[0].message.content
    return optimized_query

def optimize_query(query):
    if query :
        try:
            optimized_query = optimiser_requete(query)
            return jsonify({"optimized_query": optimized_query})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else :
        return jsonify({"error": "Query is required"}), 400
    
# Exemple d'utilisation de la fonction
#requete_sql = "SELECT prod, AVG(prix) as avg_prix FROM produits ;"
#requete_optimisee = optimiser_requete(requete_sql)
#print(requete_optimisee)  # Imprime simplement le résultat de la requête SQL optimisée
