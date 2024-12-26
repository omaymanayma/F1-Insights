from confluent_kafka import Producer
import pandas as pd
import json

# Configurer le producteur Kafka
producer = Producer({'bootstrap.servers': 'localhost:9092'})

def send_race_results_to_kafka(csv_file, topic='f1_results'):
    """Envoie les résultats de course à Kafka."""
    # Lire le fichier CSV
    df = pd.read_csv(csv_file)

    # Envoyer chaque ligne du CSV comme un message Kafka
    for index, row in df.iterrows():
        message = row.to_dict()  # Convertir la ligne en dictionnaire
        producer.produce(topic, key=str(row['Driver']), value=json.dumps(message))
  # Envoyer au topic Kafka
        print(f"Message envoyé à Kafka: {message}")

    # Fermer le producteur
    producer.flush()

# Exemple d'utilisation
if __name__ == "__main__":
    send_race_results_to_kafka('../results_2023/Bahrain_Grand_Prix.csv')
