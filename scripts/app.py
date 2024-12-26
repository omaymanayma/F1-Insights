from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Fonction pour se connecter à la base de données PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='f1',  # Remplace par le nom de ta base de données
        user='postgres',
        password='configured'  # Remplace par ton mot de passe
    )
    return conn

# Route pour obtenir des données de la base
@app.route('/api/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM <nom_de_ta_table>")  # Remplace <nom_de_ta_table> par ta table
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Transforme les résultats en format JSON
    data = []
    for row in rows:
        data.append({'id': row[0], 'column_name': row[1]})  # Remplace par les noms de tes colonnes
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
