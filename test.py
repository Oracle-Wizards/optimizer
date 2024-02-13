from flask import Flask, jsonify
import oracledb

app = Flask(__name__)

# Configuration de la base de données Oracle
oracle_connection_string = 'CO/BETTER_CO@better-sql.francecentral.cloudapp.azure.com/FREE'

# Fonction pour se connecter à la base de données Oracle
def connect_to_oracle():
    connection = oracledb.connect(oracle_connection_string)
    return connection

# Route de test pour vérifier la connexion à la base de données
@app.route('/')
def test_db_connection():
    try:
        connection = connect_to_oracle()
        connection.close()
        return jsonify({'message': 'Connexion réussie à la base de données Oracle'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
