import pandas as pd
import matplotlib.pyplot as plt
import os  # Ajout de cette ligne

def visualize_cumulative_points(season):
    """Crée un graphique des points cumulés par pilote."""
    file_name = f"full_season_{season}.csv"
    if not os.path.exists(file_name):
        print(f"Fichier {file_name} introuvable. Exécute d'abord le script de transformation.")
        return

    df = pd.read_csv(file_name)
    drivers = df["Driver"].unique()

    # Tracer les points cumulés pour chaque pilote
    plt.figure(figsize=(12, 6))
    for driver in drivers:
        driver_data = df[df["Driver"] == driver]
        plt.plot(driver_data.index, driver_data["Cumulative Points"], label=driver)

    plt.title(f"Points cumulés des pilotes - Saison {season}")
    plt.xlabel("Courses")
    plt.ylabel("Points cumulés")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# Exemple d'utilisation
if __name__ == "__main__":
    season = 2023
    visualize_cumulative_points(season)
