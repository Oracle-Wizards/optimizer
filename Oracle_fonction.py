import oracledb

oracle_connection_string = 'CO/BETTER_CO@better-sql.francecentral.cloudapp.azure.com/FREE'

# Fonction pour se connecter à la base de données Oracle
def connect_to_oracle():
    connection = oracledb.connect(oracle_connection_string)
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
