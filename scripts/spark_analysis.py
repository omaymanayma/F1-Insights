from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialiser la session Spark
spark = SparkSession.builder \
    .appName("F1 Results Analysis") \
    .getOrCreate()

# Charger les résultats depuis un fichier CSV dans un DataFrame Spark
df = spark.read.csv("full_season_2023.csv", header=True, inferSchema=True)

# Afficher les premières lignes
df.show(5)

# Exemple d'analyse: Calculer le total des points pour chaque pilote
df_grouped = df.groupBy("Driver").agg({"Points": "sum"})
df_grouped.show()

# Sauvegarder les résultats traités
df_grouped.write.csv("total_points_by_driver.csv", header=True)

# Terminer la session Spark
spark.stop()
