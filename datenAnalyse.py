import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import os
import glob


def convert_to_numeric(value):
    try:
        return float(value)
    except ValueError:
        print(f"Could not convert value: {value}")
        return np.nan


def load_and_clean_csv(file_path):
    try:
        data = pd.read_csv(file_path, on_bad_lines='skip')
        return data
    except pd.errors.ParserError as e:
        print(f"Error parsing {file_path}: {e}")
        return None


def preprocess_data(data, date_format):
    data['Month'] = pd.to_datetime(data['Month'], format=date_format, errors='coerce')
    data = data.dropna(subset=['Month'])
    data = data.sort_values('Month')
    return data


def analyze_and_plot_avg(data, output_dir, game_name):
    x_col, y_col = 'average_viewers', 'avg_players'
    correlation = data[[x_col, y_col]].corr()
    with open(os.path.join(output_dir, f'{game_name}_berechnungen.txt'), 'a') as f:
        f.write(f"Korrelation zwischen {x_col} und {y_col}:\n")
        f.write(correlation.to_string() + '\n')

    X = data[[x_col]].values.reshape(-1, 1)
    y = data[y_col].values

    regressor = LinearRegression()
    regressor.fit(X, y)
    y_pred = regressor.predict(X)

    with open(os.path.join(output_dir, f'{game_name}_berechnungen.txt'), 'a') as f:
        f.write(f"Regressionskoeffizient: {regressor.coef_[0]}\n")
        f.write(f"Intercept: {regressor.intercept_}\n")
        f.write(f"R^2: {regressor.score(X, y)}\n \n")

    plt.figure(figsize=(12, 6))
    plt.scatter(X, y, color='blue', label='Datenpunkte')
    plt.plot(X, y_pred, color='red', linewidth=2, label='Regressionslinie')
    plt.title('Lineare Regression zwischen durchschnittlichen Twitch-Zuschauern und Steam-Spielern (2023)')
    plt.xlabel('Durchschnittliche Twitch-Zuschauer')
    plt.ylabel('Durchschnittliche Steam-Spieler')
    plt.legend()
    plt.savefig(os.path.join(output_dir, f'{game_name}_regression_avg.png'))
    plt.close()


def analyze_and_plot_peak(data, output_dir, game_name):
    x_col, y_col = 'peak_viewers', 'peak_players'
    correlation = data[[x_col, y_col]].corr()
    with open(os.path.join(output_dir, f'{game_name}_berechnungen.txt'), 'a') as f:
        f.write(f"Korrelation zwischen {x_col} und {y_col}:\n")
        f.write(correlation.to_string() + '\n')

    X = data[[x_col]].values.reshape(-1, 1)
    y = data[y_col].values

    regressor = LinearRegression()
    regressor.fit(X, y)
    y_pred = regressor.predict(X)

    with open(os.path.join(output_dir, f'{game_name}_berechnungen.txt'), 'a') as f:
        f.write(f"Regressionskoeffizient: {regressor.coef_[0]}\n")
        f.write(f"Intercept: {regressor.intercept_}\n")
        f.write(f"R^2: {regressor.score(X, y)}\n")

    plt.figure(figsize=(12, 6))
    plt.scatter(X, y, color='blue', label='Datenpunkte')
    plt.plot(X, y_pred, color='red', linewidth=2, label='Regressionslinie')
    plt.title('Lineare Regression zwischen Spitzen-Twitch-Zuschauern und Spitzen-Steam-Spielern (2021-2023)')
    plt.xlabel('Spitzen-Twitch-Zuschauer')
    plt.ylabel('Spitzen-Steam-Spieler')
    plt.legend()
    plt.savefig(os.path.join(output_dir, f'{game_name}_regression_peak.png'))
    plt.close()


def plot_average_values(data, output_dir, game_name):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x='Month', y='average_viewers', label='Durchschnittliche Twitch-Zuschauer')
    sns.lineplot(data=data, x='Month', y='avg_players', label='Durchschnittliche Steam-Spieler')
    plt.title('Vergleich der durchschnittlichen Twitch-Zuschauer und Steam-Spielerzahlen (2023)')
    plt.xlabel('Monat')
    plt.ylabel('Anzahl')
    plt.legend()
    plt.savefig(os.path.join(output_dir, f'{game_name}_average_values.png'))
    plt.close()


def plot_peak_values(data, output_dir, game_name):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x='Month', y='peak_viewers', label='Spitzen-Twitch-Zuschauer')
    sns.lineplot(data=data, x='Month', y='peak_players', label='Spitzen-Steam-Spieler')
    plt.title('Vergleich der Spitzen-Twitch-Zuschauer und Spitzen-Steam-Spielerzahlen (2021-2023)')
    plt.xlabel('Monat')
    plt.ylabel('Anzahl')
    plt.legend()
    plt.savefig(os.path.join(output_dir, f'{game_name}_peak_values.png'))
    plt.close()


def process_files(twitch_files, steam_files):
    for twitch_file in twitch_files:
        for steam_file in steam_files:
            game_name_twitch = os.path.basename(twitch_file).split('_Twitch.csv')[0]
            game_name_steam = os.path.basename(steam_file).split('_Steam.csv')[0]

            # Make sure we are matching the correct game data
            if game_name_twitch != game_name_steam:
                continue

            game_name = game_name_twitch
            output_dir = os.path.join('output', game_name)
            os.makedirs(output_dir, exist_ok=True)

            twitch_data = load_and_clean_csv(twitch_file)
            steam_data = load_and_clean_csv(steam_file)

            if twitch_data is None or steam_data is None:
                print(f"Error loading data for {game_name}")
                continue

            twitch_data = preprocess_data(twitch_data, '%m/%Y')
            steam_data = preprocess_data(steam_data, '%B %Y')

            merged_data = pd.merge(twitch_data, steam_data, on='Month', how='inner')

            data_2023 = merged_data[merged_data['Month'].dt.year == 2023].copy()
            data_peak = merged_data[merged_data['Month'].dt.year.isin([2021, 2022, 2023])].copy()

            rename_columns = {
                'Average_x': 'average_viewers', 'Average_y': 'avg_players',
                'Peak_x': 'peak_viewers', 'Peak_y': 'peak_players'
            }
            data_2023.rename(columns=rename_columns, inplace=True)
            data_peak.rename(columns=rename_columns, inplace=True)

            data_2023['average_viewers'] = data_2023['average_viewers'].apply(convert_to_numeric)
            data_2023['avg_players'] = data_2023['avg_players'].apply(convert_to_numeric)
            data_peak['peak_viewers'] = data_peak['peak_viewers'].apply(convert_to_numeric)
            data_peak['peak_players'] = data_peak['peak_players'].apply(convert_to_numeric)

            data_2023.dropna(subset=['average_viewers', 'avg_players'], inplace=True)
            data_peak.dropna(subset=['peak_viewers', 'peak_players'], inplace=True)

            if not data_2023.empty:
                analyze_and_plot_avg(data_2023, output_dir, game_name)
                plot_average_values(data_2023, output_dir, game_name)

            if not data_peak.empty:
                analyze_and_plot_peak(data_peak, output_dir, game_name)
                plot_peak_values(data_peak, output_dir, game_name)


twitch_files = glob.glob('data_twitch/*_Twitch.csv')
steam_files = glob.glob('data_steam/*_Steam.csv')

process_files(twitch_files, steam_files)
