import pandas as pd
import os

def transform_race_results(season):
    """Transforme les résultats de toutes les courses pour une saison."""
    folder = f"results_{season}"
    if not os.path.exists(folder):
        print(f"Dossier {folder} introuvable. Exécute d'abord le script d'extraction.")
        return

    all_races = []
    cumulative_points = {}
    podiums = []  # Liste pour stocker les podiums

    # Parcourir tous les fichiers CSV dans le dossier
    for file_name in sorted(os.listdir(folder)):
        if file_name.endswith(".csv"):
            race_path = os.path.join(folder, file_name)
            df = pd.read_csv(race_path)
            race_name = file_name.replace(".csv", "").replace("_", " ")

            # Ajouter les points cumulés
            df["Cumulative Points"] = df["Driver"].apply(lambda driver: cumulative_points.get(driver, 0))
            for _, row in df.iterrows():
                cumulative_points[row["Driver"]] = cumulative_points.get(row["Driver"], 0) + row["Points"]

            # Ajouter des informations sur la course
            df["Race"] = race_name
            all_races.append(df)

            # Ajouter les podiums (top 3) pour chaque course
            top_3 = df.head(3)  # Les 3 premiers
            for position, row in top_3.iterrows():
                podiums.append([race_name, row["Driver"], position + 1, row["Constructor"], row["Time"]])

    # Fusionner toutes les courses
    full_season = pd.concat(all_races, ignore_index=True)

    # Sauvegarder les résultats transformés
    output_file = f"full_season_{season}.csv"
    full_season.to_csv(output_file, index=False)
    print(f"Fichier transformé sauvegardé : {output_file}")

    # Analyse des podiums
    df_podiums = pd.DataFrame(podiums, columns=["Race", "Driver", "Position", "Constructor", "Time"])
    df_podiums.to_csv(f"podiums_{season}.csv", index=False)
    print(f"Fichier des podiums sauvegardé : podiums_{season}.csv")

# Exemple d'utilisation
if __name__ == "__main__":
    season = 2023
    transform_race_results(season)
