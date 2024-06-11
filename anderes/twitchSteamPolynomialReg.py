import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
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

# Hyperparameter-Tuning und Cross-Validation
degrees = [1, 2, 3, 4, 5]
cv_scores = []

for degree in degrees:
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
    cv_scores.append(np.mean(scores))

best_degree = degrees[np.argmax(cv_scores)]
print(f'Bester Polynomgrad: {best_degree}')

# Polynomial Regression mit dem besten Grad
best_polyreg = make_pipeline(PolynomialFeatures(best_degree), LinearRegression())
best_polyreg.fit(X, y)
y_best_poly_pred = best_polyreg.predict(X)

# Visualisierung der originalen Daten und der Modellvorhersagen
plt.figure(figsize=(12, 6))
plt.scatter(X, y, color='blue', label='Datenpunkte')
plt.plot(X, y_best_poly_pred, color='red', linewidth=2, label=f'Polynomial Regression (Grad {best_degree})')
plt.title('Nicht-lineare Regression zwischen Twitch-Zuschauern und Steam-Spielern')
plt.xlabel('Durchschnittliche Twitch-Zuschauer')
plt.ylabel('Durchschnittliche Steam-Spieler')
plt.legend()
plt.show()
