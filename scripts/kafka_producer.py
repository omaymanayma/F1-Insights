from confluent_kafka import Producer
import pandas as pd
import json

# Configurer le producteur Kafka
producer = Producer({'bootstrap.servers': 'localhost:9092'})

def send_race_results_to_kafka(csv_file, race_name, topic='f1_results'):
    """Envoie les résultats d'une course spécifique à Kafka."""
    # Lire le fichier CSV
    df = pd.read_csv(csv_file)

    # Nettoyer les valeurs NaN et formats de temps, supprimer la colonne 'Time'
    df['Time'] = df['Time'].apply(lambda x: None if pd.isna(x) or not str(x).replace(":", "").isdigit() else x)
    df['Points'] = df['Points'].fillna(0).astype(int)

    # Supprimer la colonne 'Time' des données
    df = df.drop(columns=['Time'])

    # Filtrer les données pour la course spécifiée
    race_data = df[df['Race'] == race_name]

    # Envoyer chaque ligne filtrée du CSV comme un message Kafka
    for _, row in race_data.iterrows():
        message = row.to_dict()  # Convertir la ligne en dictionnaire
        producer.produce(topic, key=str(row['Driver']), value=json.dumps(message))
        print(f"Message envoyé à Kafka: {message}")

    # Fermer le producteur
    producer.flush()

# Exemple d'utilisation
if __name__ == "__main__":
    # Remplacez par le nom de la course que vous souhaitez tester
    send_race_results_to_kafka('../full_season_2023.csv', 'Australian Grand Prix')
