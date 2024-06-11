import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
import numpy as np

# Funktion zum Konvertieren von String-Werten wie "2.0K" in numerische Werte
def convert_to_numeric(value):
    if isinstance(value, str):
        if 'K' in value:
            return float(value.replace('K', '')) * 1000
        elif 'M' in value:
            return float(value.replace('M', '')) * 1000000
    return float(value)

# Dateien laden
twitch_data = pd.read_csv('../data/monthly_twitch_stardewValley.csv')
steam_data = pd.read_csv('../data/monthly_steam_stardewValley.csv')

# Konvertiere Datumsspalten zu datetime (Format explizit angeben)
twitch_data['Month'] = pd.to_datetime(twitch_data['Month'], format='%m/%Y')
steam_data['Month'] = pd.to_datetime(steam_data['Month'], format='%B %Y')

# Daten nach Monat sortieren
twitch_data = twitch_data.sort_values('Month')
steam_data = steam_data.sort_values('Month')

# Zusammenführen der Datensätze basierend auf dem Monat
merged_data = pd.merge(twitch_data, steam_data, on='Month', how='inner')

# Spalten umbenennen
merged_data.rename(columns={'Average_x': 'average_viewers', 'Average_y': 'avg_players'}, inplace=True)

# Konvertieren der Werte in numerische Werte
merged_data['average_viewers'] = merged_data['average_viewers'].apply(convert_to_numeric)
merged_data['avg_players'] = merged_data['avg_players'].apply(convert_to_numeric)

# Daten für das Modell vorbereiten
X = merged_data[['average_viewers']].values.reshape(-1, 1)
y = merged_data['avg_players'].values

# Polynomial Regression (2. Grad)
polyreg = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
polyreg.fit(X, y)
y_poly_pred = polyreg.predict(X)

# Random Forest Regression
forest = RandomForestRegressor()
forest.fit(X, y)
y_forest_pred = forest.predict(X)

# Support Vector Regression
svr = SVR(kernel='rbf')
svr.fit(X, y)
y_svr_pred = svr.predict(X)

# Visualisierung der originalen Daten und der Modellvorhersagen
plt.figure(figsize=(12, 6))
plt.scatter(X, y, color='blue', label='Datenpunkte')
plt.plot(X, y_poly_pred, color='red', linewidth=2, label='Polynomial Regression (2. Grad)')
plt.plot(X, y_forest_pred, color='green', linewidth=2, label='Random Forest Regression')
plt.plot(X, y_svr_pred, color='purple', linewidth=2, label='Support Vector Regression')
plt.title('Nicht-lineare Regression zwischen Twitch-Zuschauern und Steam-Spielern')
plt.xlabel('Durchschnittliche Twitch-Zuschauer')
plt.ylabel('Durchschnittliche Steam-Spieler')
plt.legend()
plt.show()
