from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, String, Integer
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

# Créer une session Spark
spark = SparkSession.builder.appName("F1 Kafka Stream").getOrCreate()

# Créer un contexte de streaming Spark
ssc = StreamingContext(spark.sparkContext, 1)  # Intervalle de 1 seconde

# Définir le schema de notre message Kafka
schema = StructType([
    StructField("Driver", String(), True),
    StructField("Points", Integer(), True),
    StructField("Race", String(), True)
])

# Connecter Spark Streaming à Kafka
kafka_stream = KafkaUtils.createStream(ssc, 'localhost:2181', 'f1_group', {'f1_results': 1})

# Extraire les messages Kafka du flux
messages = kafka_stream.map(lambda x: x[1])  # x[1] contient les messages

# Convertir les messages JSON en DataFrame
df = messages.map(lambda x: spark.read.json(x, schema))

# Effectuer une analyse, par exemple, calculer le total des points pour chaque pilote
df_grouped = df.groupBy("Driver").agg({"Points": "sum"})

# Afficher les résultats
df_grouped.pprint()

# Démarrer le flux
ssc.start()
ssc.awaitTermination()
