import requests
import pandas as pd
import os

def get_race_results(season, round_number):
    """Récupère les résultats d'une course donnée via l'API Ergast."""
    url = f"https://ergast.com/api/f1/{season}/{round_number}/results.json"
    print(f"Requête vers : {url}")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        races = data['MRData']['RaceTable']['Races']
        if races:
            race = races[0]
            race_name = race['raceName']
            date = race['date']
            results = [
                {
                    "Position": result['position'],
                    "Driver": f"{result['Driver']['givenName']} {result['Driver']['familyName']}",
                    "Constructor": result['Constructor']['name'],
                    "Time": result.get('Time', {}).get('time', "N/A"),
                    "Points": result['points']
                }
                for result in race['Results']
            ]
            return pd.DataFrame(results), race_name, date
    return None, None, None

def get_all_race_results(season):
    """Récupère les résultats de toutes les courses d'une saison."""
    print(f"Récupération des résultats pour la saison {season}...")
    os.makedirs(f"results_{season}", exist_ok=True)  # Créer un dossier pour la saison
    for round_number in range(1, 23):  # Maximum 22 courses par saison
        df, race_name, date = get_race_results(season, round_number)
        if df is not None:
            file_name = f"results_{season}/{race_name.replace(' ', '_')}.csv"
            df.to_csv(file_name, index=False)
            print(f"Résultats sauvegardés : {file_name}")
        else:
            print(f"Fin de la saison après {round_number - 1} courses.")
            break

# Exemple d'utilisation
if __name__ == "__main__":
    season = 2023
    get_all_race_results(season)
