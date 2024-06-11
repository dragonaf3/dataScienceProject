import os
import pandas as pd


def remove_spaces_in_month(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)
            df = pd.read_csv(file_path)

            if 'Month' in df.columns:
                df['Month'] = df['Month'].str.replace(' ', '')

            output_file_path = os.path.join(output_folder, filename)
            df.to_csv(output_file_path, index=False)


input_folder = 'data_twitch'
output_folder = 'cleanedData_twitch'
remove_spaces_in_month(input_folder, output_folder)
