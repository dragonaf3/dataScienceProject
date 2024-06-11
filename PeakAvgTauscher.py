import os
import pandas as pd


def swap_peak_average(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)
            df = pd.read_csv(file_path)

            if 'Peak' in df.columns and 'Average' in df.columns:
                df[['Peak', 'Average']] = df[['Average', 'Peak']]

            output_path = os.path.join(output_folder, filename)
            df.to_csv(output_path, index=False)
            print(f"Processed {filename} and saved to {output_path}")


input_folder = "data_twitch"
output_folder = "cleanedData_twitch"

swap_peak_average(input_folder, output_folder)
