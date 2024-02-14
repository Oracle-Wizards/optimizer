import oracledb
import os
from dotenv import load_dotenv

# Fonction pour se connecter à la base de données Oracle
def connect_to_oracle():
    load_dotenv()
    ORACLE_CNX_KEY = os.getenv('oracle_connection_string')
    connection = oracledb.connect(ORACLE_CNX_KEY)
    return connection


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
