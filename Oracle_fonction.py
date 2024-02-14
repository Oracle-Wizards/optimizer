import oracledb
import os
from dotenv import load_dotenv

# Fonction pour se connecter à la base de données Oracle
def connect_to_oracle():
    load_dotenv()
    ORACLE_CNX_KEY = os.getenv('oracle_connection_string')
    connection = oracledb.connect(ORACLE_CNX_KEY)
    return connection


def getTables():
    connection = connect_to_oracle()
    cursor = connection.cursor()

    # Exécution de la requête SQL pour récupérer la liste des tables
    cursor.execute("SELECT table_name FROM user_tables")

    # Récupération des résultats
    tables = [row[0] for row in cursor.fetchall()]

    # Fermeture du curseur et de la connexion
    cursor.close()
    connection.close()

    return tables
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

def executionquery(sql_query):
    connection = connect_to_oracle()
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
