import psycopg2
from confluent_kafka import Consumer, KafkaException
import json

# Connexion à PostgreSQL
conn = psycopg2.connect("dbname=test user=postgres password=password")
cursor = conn.cursor()

# Configuration du consommateur Kafka
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'f1_consumer_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

# S'abonner au topic 'f1_race_results'
consumer.subscribe(['f1_race_results'])

# Fonction pour insérer des résultats dans la base de données
def insert_data(data):
    cursor.execute("""
        INSERT INTO race_results (race, position, driver, constructor, time, points) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data['Race'], data['Position'], data['Driver'], data['Constructor'], data['Time'], data['Points']))
    conn.commit()

# Consommer les messages en temps réel
def consume_messages():
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                race_data = json.loads(msg.value().decode('utf-8'))
                insert_data(race_data)
                print(f"Inserted into DB: {race_data}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        conn.close()

consume_messages()
