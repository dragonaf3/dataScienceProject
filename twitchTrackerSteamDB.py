import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


# Funktion zum Konvertieren von String-Werten wie "2.0K" in numerische Werte
def convert_to_numeric(value):
    if isinstance(value, str):
        value = value.replace(',', '')  # Entferne Kommas
        if '-' in value or value == '':
            return np.nan
        if 'K' in value:
            return float(value.replace('K', '')) * 1000
        elif 'M' in value:
            return float(value.replace('M', '')) * 1000000
    try:
        return float(value)
    except ValueError:
        print(f"Could not convert value: {value}")
        return np.nan


# Funktion zum Laden und Bereinigen der CSV-Datei
def load_and_clean_csv(file_path):
    try:
        data = pd.read_csv(file_path, on_bad_lines='skip')  # Fehlerhafte Zeilen überspringen
        return data
    except pd.errors.ParserError as e:
        print(f"Error parsing {file_path}: {e}")
        return None


# Dateien laden und überprüfen
twitch_data = load_and_clean_csv('data/Apex_Legends_Twitch.csv')
steam_data = load_and_clean_csv('data/Apex_Legends_Steam.csv')

if twitch_data is None or steam_data is None:
    print("Ein Fehler ist beim Laden der Daten aufgetreten.")
else:
    # Spaltennamen anzeigen
    print("Twitch Data Columns:", twitch_data.columns)
    print("Steam Data Columns:", steam_data.columns)

    # Konvertiere Datumsspalten zu datetime (Format explizit angeben)
    twitch_data['Month'] = pd.to_datetime(twitch_data['Month'], format='%m/%Y', errors='coerce')
    steam_data['Month'] = pd.to_datetime(steam_data['Month'], format='%B %Y', errors='coerce')

    # Entferne Zeilen mit ungültigen Datumswerten
    twitch_data = twitch_data.dropna(subset=['Month'])
    steam_data = steam_data.dropna(subset=['Month'])

    # Daten nach Monat sortieren
    twitch_data = twitch_data.sort_values('Month')
    steam_data = steam_data.sort_values('Month')

    # Zusammenführen der Datensätze basierend auf dem Monat
    merged_data = pd.merge(twitch_data, steam_data, on='Month', how='inner')

    # Filtern nach Jahr 2023 für die durchschnittlichen Werte
    data_2023 = merged_data[merged_data['Month'].dt.year == 2023].copy()

    # Filtern nach den Jahren 2021, 2022 und 2023 für die Spitzenwerte
    data_peak = merged_data[merged_data['Month'].dt.year.isin([2021, 2022, 2023])].copy()

    # Spalten umbenennen
    data_2023.rename(columns={'Average_x': 'average_viewers', 'Average_y': 'avg_players', 'Peak_x': 'peak_viewers',
                              'Peak_y': 'peak_players'}, inplace=True)
    data_peak.rename(columns={'Average_x': 'average_viewers', 'Average_y': 'avg_players', 'Peak_x': 'peak_viewers',
                              'Peak_y': 'peak_players'}, inplace=True)

    # Konvertieren der Werte in numerische Werte
    data_2023['average_viewers'] = data_2023['average_viewers'].apply(convert_to_numeric)
    data_2023['avg_players'] = data_2023['avg_players'].apply(convert_to_numeric)
    data_peak['peak_viewers'] = data_peak['peak_viewers'].apply(convert_to_numeric)
    data_peak['peak_players'] = data_peak['peak_players'].apply(convert_to_numeric)

    # Überprüfen, ob die Spalten existieren
    print("Merged Data Columns:", merged_data.columns)

    # Daten vor dem Entfernen von NaNs anzeigen
    print("Data 2023 Head Before Dropping NaNs:")
    print(data_2023.head())
    print("Data Peak Head Before Dropping NaNs:")
    print(data_peak.head())

    # Fehlende Werte behandeln (z.B. Zeilen mit NaNs entfernen)
    data_2023.dropna(subset=['average_viewers', 'avg_players'], inplace=True)
    data_peak.dropna(subset=['peak_viewers', 'peak_players'], inplace=True)

    # Daten nach dem Entfernen von NaNs anzeigen
    print("Data 2023 Head After Dropping NaNs:")
    print(data_2023.head())
    print("Data Peak Head After Dropping NaNs:")
    print(data_peak.head())

    # Überprüfen, ob noch Zeilen für die Analyse übrig sind
    if data_2023.empty:
        print("No valid data available for analysis after handling missing values (2023).")
    else:
        # Korrelation berechnen (durchschnittliche Werte)
        correlation_avg = data_2023[['average_viewers', 'avg_players']].corr()
        print("Korrelation zwischen durchschnittlichen Twitch-Zuschauern und Steam-Spielern (2023):")
        print(correlation_avg)

        # Lineare Regression (durchschnittliche Werte)
        X_avg = data_2023[['average_viewers']].values.reshape(-1, 1)
        y_avg = data_2023['avg_players'].values

        regressor_avg = LinearRegression()
        regressor_avg.fit(X_avg, y_avg)

        # Vorhersagen (durchschnittliche Werte)
        y_pred_avg = regressor_avg.predict(X_avg)

        # Regressionsergebnisse (durchschnittliche Werte)
        print(f"Regressionskoeffizient (durchschnittlich): {regressor_avg.coef_[0]}")
        print(f"Intercept (durchschnittlich): {regressor_avg.intercept_}")
        print(f"R^2 (durchschnittlich): {regressor_avg.score(X_avg, y_avg)}")

        # Visualisierung (durchschnittliche Werte)
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=data_2023, x='Month', y='average_viewers', label='Durchschnittliche Twitch-Zuschauer')
        sns.lineplot(data=data_2023, x='Month', y='avg_players', label='Durchschnittliche Steam-Spieler')
        plt.title('Vergleich der durchschnittlichen Twitch-Zuschauer und Steam-Spielerzahlen (2023)')
        plt.xlabel('Monat')
        plt.ylabel('Anzahl')
        plt.legend()
        plt.show()

        # Scatterplot und Regressionslinie (durchschnittliche Werte)
        plt.figure(figsize=(12, 6))
        plt.scatter(X_avg, y_avg, color='blue', label='Datenpunkte')
        plt.plot(X_avg, y_pred_avg, color='red', linewidth=2, label='Regressionslinie')
        plt.title('Lineare Regression zwischen durchschnittlichen Twitch-Zuschauern und Steam-Spielern (2023)')
        plt.xlabel('Durchschnittliche Twitch-Zuschauer')
        plt.ylabel('Durchschnittliche Steam-Spieler')
        plt.legend()
        plt.show()

    if data_peak.empty:
        print("No valid data available for analysis after handling missing values (Peak).")
    else:
        # Korrelation berechnen (Spitzenwerte)
        correlation_peak = data_peak[['peak_viewers', 'peak_players']].corr()
        print("Korrelation zwischen Spitzen-Twitch-Zuschauern und Spitzen-Steam-Spielern (2021-2023):")
        print(correlation_peak)

        # Lineare Regression (Spitzenwerte)
        X_peak = data_peak[['peak_viewers']].values.reshape(-1, 1)
        y_peak = data_peak['peak_players'].values

        regressor_peak = LinearRegression()
        regressor_peak.fit(X_peak, y_peak)

        # Vorhersagen (Spitzenwerte)
        y_pred_peak = regressor_peak.predict(X_peak)

        # Regressionsergebnisse (Spitzenwerte)
        print(f"Regressionskoeffizient (Spitzenwerte): {regressor_peak.coef_[0]}")
        print(f"Intercept (Spitzenwerte): {regressor_peak.intercept_}")
        print(f"R^2 (Spitzenwerte): {regressor_peak.score(X_peak, y_peak)}")

        # Visualisierung (Spitzenwerte)
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=data_peak, x='Month', y='peak_viewers', label='Spitzen-Twitch-Zuschauer')
        sns.lineplot(data=data_peak, x='Month', y='peak_players', label='Spitzen-Steam-Spieler')
        plt.title('Vergleich der Spitzen-Twitch-Zuschauer und Spitzen-Steam-Spielerzahlen (2021-2023)')
        plt.xlabel('Monat')
        plt.ylabel('Anzahl')
        plt.legend()
        plt.show()

        # Scatterplot und Regressionslinie (Spitzenwerte)
        plt.figure(figsize=(12, 6))
        plt.scatter(X_peak, y_peak, color='blue', label='Datenpunkte')
        plt.plot(X_peak, y_pred_peak, color='red', linewidth=2, label='Regressionslinie')
        plt.title('Lineare Regression zwischen Spitzen-Twitch-Zuschauern und Spitzen-Steam-Spielern (2021-2023)')
        plt.xlabel('Spitzen-Twitch-Zuschauer')
        plt.ylabel('Spitzen-Steam-Spieler')
        plt.legend()
        plt.show()
