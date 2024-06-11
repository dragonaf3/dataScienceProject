import os
import pandas as pd

input_directory = 'data_steam'
output_directory = 'cleanedData_steam'


def clean_csv(file_path, output_path):
    data = pd.read_csv(file_path)

    if 'Peak' in data.columns and data['Peak'].dtype == 'object':
        data['Peak'] = pd.to_numeric(data['Peak'].str.replace(',', ''), errors='coerce')
    if 'Average' in data.columns and data['Average'].dtype == 'object':
        data['Average'] = pd.to_numeric(data['Average'].str.replace(',', ''), errors='coerce')

    if all(col in data.columns for col in ['Month', 'Peak', 'Average']):
        cleaned_data = data[['Month', 'Peak', 'Average']]
        cleaned_data = cleaned_data.fillna('-')
        cleaned_data.to_csv(output_path, index=False)


os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename)
        clean_csv(file_path, output_path)
