from flask import Flask,request,render_template
from openai import OpenAI
import re
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()



# Initialiser le client OpenAI
client = OpenAI(
    api_key=os.getenv('llama_key'),
    base_url="https://api.llama-api.com"
)

# Fonction pour optimiser la requête SQL
def optimiser_requete(requete_sql):
    response = client.chat.completions.create(
        model="llama-13b-chat",
        messages=[
            {"role": "system", "content": "Optimize the following SQL query format the output query in this  ```   ```  and give me just query optimised :"},
            {"role": "user", "content": requete_sql}
        ]
    )
    return response.choices[0].message.content

# Exemple d'utilisation de la fonction
requete_sql = "select t3.name, t3.time from train_station as t1 join station as t2 on t1.station_id = t2.id join train as t3 on t3.train_id = t1.train_id where t1.station_id = 1;"
#requete_optimisee = optimiser_requete(requete_sql)
#print(requete_optimisee)  # Imprime simplement le résultat de la requête SQL optimisée



def extract_optimized_query(output):
    # Define the pattern to match the SQL query within the output string
    #pattern = r'([^`]*)'
    pattern = r'```(.*)```'
    
    # Use regular expression to find the SQL query
    match = re.search(pattern, output, re.DOTALL)
    
    # If a match is found, return the optimized SQL query
    if match:
        return match.group(1).strip()
    else:
        return None
        

@app.route('/')
def index():
    return f"<h1>{ extract_optimized_query(str(optimiser_requete(requete_sql)))}</h1>"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)