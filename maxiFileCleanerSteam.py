import os
import pandas as pd
from datetime import datetime


def convert_month_format(input_folder, output_folder, date_format='%Y-%m-%d'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)
            df = pd.read_csv(file_path)

            if 'Month' in df.columns:
                df['Month'] = pd.to_datetime(df['Month'], format=date_format, errors='coerce').dt.strftime('%B %Y')

            if 'Peak' in df.columns and 'Average' in df.columns:
                df['Peak'] = df['Peak'].astype(str).str.replace('.', '').replace('-', '0').astype(int)
                df['Average'] = df['Average'].astype(str).str.replace('.', '').replace('-', '0').astype(int)

            output_file_path = os.path.join(output_folder, filename)
            df.to_csv(output_file_path, index=False)


input_folder = 'data_steam'
output_folder = 'cleanedData_steam'
date_format = '%m/%Y'
convert_month_format(input_folder, output_folder, date_format)
