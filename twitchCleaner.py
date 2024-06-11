import os
import pandas as pd

input_directory = 'data_twitch'
output_directory = 'cleanedData_twitch'


def convert_to_number(value):
    if isinstance(value, str):
        value = value.lower()
        if 'k' in value:
            return float(value.replace('k', '')) * 1000
        if 'm' in value:
            return float(value.replace('m', '')) * 1000000
        return float(value.replace(',', ''))
    return value


def clean_twitch_csv(file_path, output_path):
    data = pd.read_csv(file_path)

    if 'Peak' in data.columns:
        data['Peak'] = data['Peak'].apply(convert_to_number)
        data['Peak'] = pd.to_numeric(data['Peak'], errors='coerce')
    if 'Average' in data.columns:
        data['Average'] = data['Average'].apply(convert_to_number)
        data['Average'] = pd.to_numeric(data['Average'], errors='coerce')

    if all(col in data.columns for col in ['Month', 'Peak', 'Average']):
        cleaned_data = data[['Month', 'Peak', 'Average']]
        cleaned_data = cleaned_data.fillna('-')
        cleaned_data.to_csv(output_path, index=False)


os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename)
        clean_twitch_csv(file_path, output_path)
