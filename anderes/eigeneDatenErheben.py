import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr


# Funktion zum Abrufen eines neuen Access-Tokens
def get_new_access_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    return response.json()['access_token']


# Funktion zum Abrufen der Spiel-ID von Twitch
def get_game_id(game_name, client_id, access_token):
    url = 'https://api.twitch.tv/helix/games'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'name': game_name
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if 'data' in data and len(data['data']) > 0:
        return data['data'][0]['id']
    else:
        print(f"Could not find game ID for {game_name}")
        return None


# Funktion zum Abrufen der Twitch-Daten
def get_twitch_data(game_id, client_id, access_token):
    url = f"https://api.twitch.tv/helix/streams?game_id={game_id}"
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)

    # Debugging: Ausgeben der API-Antwort
    print(f"Twitch API Response for game_id {game_id}: {response.json()}")

    data = response.json()

    # Check if 'data' key exists in response
    streams = data.get('data', [])

    return pd.DataFrame(streams)


# Funktion zum Abrufen der Steam-Daten
def get_steam_data(app_id):
    url = f"http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}"
    response = requests.get(url)

    # Debugging: Ausgeben der API-Antwort
    print(f"Steam API Response for app_id {app_id}: {response.json()}")

    data = response.json()
    player_count = data['response']['player_count']
    return player_count


# Twitch API-Zugangsdaten (diese müssen vorher erstellt werden)
client_id = 'l5ao2sc8v602pkvssu6y9guridtv1k'
client_secret = 'hygvjja5rw8yauobsgcbm6r2lyp07n'

# Neuen Access-Token abrufen
access_token = get_new_access_token(client_id, client_secret)
print(f'New Access Token: {access_token}')

# Beispiel-Spiele und ihre Steam-IDs und Twitch-IDs
games = {
    # 'Among Us': {'steam_id': 945360, 'twitch_id': '510683'},
    'Stardew Valley': {'steam_id': 413150, 'twitch_id': get_game_id('Stardew Valley', client_id, access_token)},
}

# Daten abrufen
twitch_data = {}
steam_data = {}

for game, ids in games.items():
    twitch_data[game] = get_twitch_data(ids['twitch_id'], client_id, access_token)
    steam_data[game] = get_steam_data(ids['steam_id'])

# Beispielhafte Verarbeitung und Analyse der Daten
for game in games.keys():
    # Daten von Twitch analysieren
    twitch_df = twitch_data[game]
    if 'viewer_count' not in twitch_df.columns:
        print(f"No viewer_count column in data for game: {game}")
        continue
    avg_viewers = twitch_df['viewer_count'].mean()
    max_viewers = twitch_df['viewer_count'].max()
    print(f"{game} - Durchschnittliche Zuschauer: {avg_viewers}, Maximale Zuschauer: {max_viewers}")

    # Daten von Steam analysieren
    current_players = steam_data[game]
    print(f"{game} - Aktuelle Spielerzahl: {current_players}")

    # Einfache Korrelation zwischen Twitch-Zuschauern und Steam-Spielern (Beispiel)
    if len(twitch_df) > 1 and len(set(twitch_df['viewer_count'])) > 1:
        viewers = twitch_df['viewer_count']
        if np.var(viewers) != 0 and np.var([current_players] * len(viewers)) != 0:
            corr, _ = pearsonr(viewers, [current_players] * len(viewers))
            print(f"{game} - Korrelation zwischen Twitch-Zuschauern und Steam-Spielern: {corr}")
        else:
            print(f"{game} - Nicht genug Varianz in den Daten für eine Korrelation.")
    else:
        print(f"{game} - Nicht genug Varianz in den Daten für eine Korrelation.")

# Visualisierung der Daten
for game in games.keys():
    twitch_df = twitch_data[game]
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=twitch_df, x='started_at', y='viewer_count')
    plt.title(f'Twitch Viewers for {game} Over Time')
    plt.xlabel('Time')
    plt.ylabel('Viewers')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
