import pandas as pd
import matplotlib.pyplot as plt
import os


def analyze_podiums(season):
    """Analyse des podiums pour la saison donnée."""
    # Charger les résultats des podiums
    podium_file = f"podiums_{season}.csv"
    if not os.path.exists(podium_file):
        print(f"Fichier {podium_file} introuvable. Assurez-vous d'exécuter le script de transformation d'abord.")
        return

    df_podiums = pd.read_csv(podium_file)

    # Nombre de podiums par pilote
    driver_podiums = df_podiums["Driver"].value_counts().reset_index()
    driver_podiums.columns = ["Driver", "Podiums"]

    # Nombre de podiums par constructeur
    constructor_podiums = df_podiums["Constructor"].value_counts().reset_index()
    constructor_podiums.columns = ["Constructor", "Podiums"]

    # Afficher les résultats
    print("Top 10 des pilotes avec le plus de podiums :")
    print(driver_podiums.head(10))
    
    print("\nTop 10 des constructeurs avec le plus de podiums :")
    print(constructor_podiums.head(10))

    # Visualiser les pilotes avec le plus de podiums
    plt.figure(figsize=(10, 6))
    plt.bar(driver_podiums["Driver"].head(10), driver_podiums["Podiums"].head(10), color="skyblue")
    plt.title("Top 10 des pilotes avec le plus de podiums")
    plt.xlabel("Pilote")
    plt.ylabel("Nombre de podiums")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"top_10_drivers_{season}.png")
    plt.show()

    # Visualiser les constructeurs avec le plus de podiums
    plt.figure(figsize=(10, 6))
    plt.bar(constructor_podiums["Constructor"].head(10), constructor_podiums["Podiums"].head(10), color="lightcoral")
    plt.title("Top 10 des constructeurs avec le plus de podiums")
    plt.xlabel("Constructeur")
    plt.ylabel("Nombre de podiums")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"top_10_constructors_{season}.png")
    plt.show()

# Exemple d'utilisation
if __name__ == "__main__":
    season = 2023
    analyze_podiums(season)
