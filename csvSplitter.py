import os
import pandas as pd

output_folder = 'cleanedData_steam'


def split_csv(file_path, output_folder):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    game_data = {}
    current_game = None

    for line in lines:
        if not line.strip():
            continue
        if ',' not in line:
            current_game = line.strip()
            game_data[current_game] = []
        else:
            game_data[current_game].append(line.strip())

    os.makedirs(output_folder, exist_ok=True)

    for game, data in game_data.items():
        if data:

            columns = data[0].split(',')

            cleaned_data = []
            for row in data[1:]:
                split_row = row.split(',')
                if len(split_row) == len(columns):
                    cleaned_data.append(split_row)
                else:

                    combined_row = []
                    for part in split_row:
                        if part:
                            combined_row.append(part)
                    cleaned_data.append(combined_row[:len(columns)])

            df = pd.DataFrame(cleaned_data, columns=columns)
            output_file = os.path.join(output_folder, f"{game.replace(' ', '_').lower()}_steam.csv")
            df.to_csv(output_file, index=False)
            print(f"Datei '{output_file}' wurde erfolgreich erstellt.")


file_path = 'data_steam/SteamDB.csv'
split_csv(file_path, output_folder)
