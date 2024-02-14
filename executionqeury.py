import google.generativeai as genai
import oracledb
from load_model import load_model

oracle_connection_string = 'CO/BETTER_CO@better-sql.francecentral.cloudapp.azure.com/FREE'

# Charger le modèle
model = load_model()

# Fonction pour exécuter une requête SQL dans Oracle
def executionquery(sql_query):
    connection = oracledb.connect(oracle_connection_string)
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()

    # Afficher le résultat de la requête SQL
    print("Résultat de la requête SQL:")
    for row in result:
        print(row)


    cursor.close()
    connection.close()

    # Retourner le résultat de la requête et l'explication
    return {"result": result}
