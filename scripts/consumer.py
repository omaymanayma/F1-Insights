import json
from confluent_kafka import Consumer, KafkaException
import psycopg2

# Connexion à Kafka
consumer = Consumer(
    {
        'bootstrap.servers': 'localhost:9092',  # Assurez-vous que le port est correct
        'group.id': 'f1_consumer_group',
        'auto.offset.reset': 'earliest',
    }
)

# S'abonner au topic
consumer.subscribe(['f1_results'])

# Connexion à PostgreSQL
conn = psycopg2.connect(
    dbname="f1", 
    user="postgres", 
    password="password", 
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

# Fonction pour insérer des données dans la base PostgreSQL sans la colonne 'time'
def insert_data(message):
    data = json.loads(message)
    position = data.get('Position')
    driver = data.get('Driver')
    constructor = data.get('Constructor')
    points = data.get('Points')
    race = data.get('Race')  # Nouvelle colonne Race

    # Insérer dans la table f1 sans la colonne 'time'
    cur.execute("""
        INSERT INTO f1 (position, driver, constructor, points, race)
        VALUES (%s, %s, %s, %s, %s)
    """, (position, driver, constructor, points, race))
    conn.commit()

# Consommer les messages de Kafka et insérer dans PostgreSQL
try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Attente des nouveaux messages
        
        if msg is None:
            continue  # Aucun message, on continue
        
        if msg.error():
            raise KafkaException(msg.error())  # Gérer les erreurs Kafka
        
        # Traiter le message
        insert_data(msg.value().decode('utf-8'))

except KeyboardInterrupt:
    pass
finally:
    # Fermer les connexions
    consumer.close()
    cur.close()
    conn.close()
