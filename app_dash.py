import dash
from dash import dash_table, html, dcc
import pandas as pd
import plotly.express as px

# Charger le fichier CSV avec les données de la saison F1
df = pd.read_csv("full_season_2023.csv")

# Calculer les points cumulés par conducteur
df['Cumulative Points'] = df.groupby('Driver')['Points'].cumsum()

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Créer un graphique des points cumulés
fig = px.line(df, x='Race', y='Cumulative Points', color='Driver', 
              title="Points cumulés par conducteur au fil des courses")

# Résumé des Top 5 conducteurs par points
top_5 = df.groupby('Race').apply(lambda x: x.nlargest(5, 'Points')).reset_index(drop=True)

# Disposition de l'application Dash
app.layout = html.Div([
    html.H1("Résultats de la Saison F1 2023"),
    
    # Affichage du graphique des points cumulés
    dcc.Graph(figure=fig),  
    
    # Table des Top 5 conducteurs
    html.H3("Top 5 Conducteurs à Chaque Course"),
    dash_table.DataTable(
        id='top5-table',
        columns=[{"name": col, "id": col} for col in top_5.columns],
        data=top_5.to_dict('records'),
        style_table={'height': '400px', 'overflowY': 'auto'},
        filter_action='native',  # Activer la recherche
        sort_action='native',    # Activer le tri
        page_size=5  # Afficher 5 lignes
    ),
    
    # Résumé des Top conducteurs de la saison
    html.H3("Résumé des Top Conducteurs de la Saison"),
    dash_table.DataTable(
        id='summary-table',
        columns=[{"name": col, "id": col} for col in df.groupby('Driver').agg(
            Total_Points=('Points', 'sum'),
            Wins=('Position', lambda x: (x == 1).sum())
        ).reset_index().columns],
        data=df.groupby('Driver').agg(
            Total_Points=('Points', 'sum'),
            Wins=('Position', lambda x: (x == 1).sum())
        ).reset_index().to_dict('records'),
        style_table={'height': '400px', 'overflowY': 'auto'},
        filter_action='native',  # Recherche dans le tableau
        sort_action='native',    # Tri du tableau
        page_size=10  # Afficher 10 lignes
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
