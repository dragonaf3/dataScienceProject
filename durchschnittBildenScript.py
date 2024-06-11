import os
import re
import numpy as np


def extract_values(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    average_viewers_match = re.search(
        r'Korrelation zwischen average_viewers und avg_players:.*?avg_players\s+([-\d.]+)', content, re.DOTALL)
    regression_coeff_avg_match = re.search(
        r'Korrelation zwischen average_viewers und avg_players:.*?Regressionskoeffizient: ([-\d.]+)', content,
        re.DOTALL)
    intercept_avg_match = re.search(r'Korrelation zwischen average_viewers und avg_players:.*?Intercept: ([-\d.]+)',
                                    content, re.DOTALL)
    r_squared_avg_match = re.search(r'Korrelation zwischen average_viewers und avg_players:.*?R\^2: ([-\d.]+)', content,
                                    re.DOTALL)

    peak_viewers_match = re.search(r'Korrelation zwischen peak_viewers und peak_players:.*?peak_players\s+([-\d.]+)',
                                   content, re.DOTALL)
    regression_coeff_peak_match = re.search(
        r'Korrelation zwischen peak_viewers und peak_players:.*?Regressionskoeffizient: ([-\d.]+)', content, re.DOTALL)
    intercept_peak_match = re.search(r'Korrelation zwischen peak_viewers und peak_players:.*?Intercept: ([-\d.]+)',
                                     content, re.DOTALL)
    r_squared_peak_match = re.search(r'Korrelation zwischen peak_viewers und peak_players:.*?R\^2: ([-\d.]+)', content,
                                     re.DOTALL)

    if all([average_viewers_match, regression_coeff_avg_match, intercept_avg_match, r_squared_avg_match,
            peak_viewers_match, regression_coeff_peak_match, intercept_peak_match, r_squared_peak_match]):
        return {
            'avg_players': float(average_viewers_match.group(1)),
            'regression_coeff_avg': float(regression_coeff_avg_match.group(1)),
            'intercept_avg': float(intercept_avg_match.group(1)),
            'r_squared_avg': float(r_squared_avg_match.group(1)),
            'peak_players': float(peak_viewers_match.group(1)),
            'regression_coeff_peak': float(regression_coeff_peak_match.group(1)),
            'intercept_peak': float(intercept_peak_match.group(1)),
            'r_squared_peak': float(r_squared_peak_match.group(1))
        }
    else:
        return None


def process_files(directory):
    all_values = {
        'avg_players': [],
        'regression_coeff_avg': [],
        'intercept_avg': [],
        'r_squared_avg': [],
        'peak_players': [],
        'regression_coeff_peak': [],
        'intercept_peak': [],
        'r_squared_peak': []
    }

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            values = extract_values(file_path)
            if values:
                for key in all_values:
                    all_values[key].append(values[key])

    averages = {key: np.mean(all_values[key]) for key in all_values if all_values[key]}
    return averages


def save_results(results, output_file):
    with open(output_file, 'w') as file:
        file.write("Korrelation zwischen average_viewers und avg_players:\n")
        file.write("                 average_viewers  avg_players\n")
        file.write(f"average_viewers         1.000000    {results['avg_players']:.6f}\n")
        file.write(f"avg_players            {results['avg_players']:.6f}     1.000000\n")
        file.write(f"Regressionskoeffizient: {results['regression_coeff_avg']}\n")
        file.write(f"Intercept: {results['intercept_avg']}\n")
        file.write(f"R^2: {results['r_squared_avg']}\n")
        file.write("\nKorrelation zwischen peak_viewers und peak_players:\n")
        file.write("              peak_viewers  peak_players\n")
        file.write(f"peak_viewers      1.000000      {results['peak_players']:.6f}\n")
        file.write(f"peak_players      {results['peak_players']:.6f}      1.000000\n")
        file.write(f"Regressionskoeffizient: {results['regression_coeff_peak']}\n")
        file.write(f"Intercept: {results['intercept_peak']}\n")
        file.write(f"R^2: {results['r_squared_peak']}\n")


directory_path = 'analysisData'
average_values = process_files(directory_path)
output_file_path = 'output/average_results.txt'
save_results(average_values, output_file_path)
print(f'Results have been written to {output_file_path}')
