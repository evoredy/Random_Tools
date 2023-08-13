import sys
import os
import pandas as pd
import pyexcel
import openpyxl
import xlrd  # Required library for reading XLS files

# Required libraries:
# - pandas: pip install pandas
# - pyexcel: pip install pyexcel
# - openpyxl: pip install openpyxl (for reading and writing XLSX files)
# - xlrd: pip install xlrd (for reading XLS files)

def flatten_json(json_data, parent_key='', sep='_'):
    flattened = {}
    for key, value in json_data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened.update(flatten_json(value, new_key, sep=sep))
        else:
            flattened[new_key] = value
    return flattened

def convert_json_to_output(input_file, output_file, to_json=False):
    if input_file.lower().endswith('.json'):
        with open(input_file, 'r') as file:
            json_data = file.read()
        data = pd.read_json(json_data)
    else:
        if input_file.lower().endswith('.csv'):
            data = pd.read_csv(input_file)
        elif input_file.lower().endswith('.xls'):
            data = pd.read_excel(input_file, engine='xlrd')
        elif input_file.lower().endswith('.xlsx'):
            data = pd.read_excel(input_file)
        elif input_file.lower().endswith('.ods'):
            data = pyexcel.get_array(file_name=input_file)
        else:
            print("Invalid input file extension. Please provide a file with the extension '.json', '.csv', '.xls', '.xlsx', or '.ods'.")
            return
    
    flattened_data = []
    for _, row in data.iterrows():
        flattened_row = flatten_json(row)
        flattened_data.append(flattened_row)
    
    df = pd.DataFrame(flattened_data)
    
    output_ext = os.path.splitext(output_file)[1].lower()
    if to_json:
        if output_ext == '.json':
            df.to_json(output_file, orient='records', indent=4)
            print("CSV/XLS/XLSX/ODS converted to prettified JSON. Output file:", output_file)
        else:
            print("Invalid output file extension. Please provide a file with the extension '.json'.")
    else:
        if input_file.lower().endswith('.json'):
            if output_ext == '.csv':
                df.to_csv(output_file, index=False)
                print("JSON converted to CSV. Output file:", output_file)
            elif output_ext == '.xlsx':
                df.to_excel(output_file, index=False)
                print("JSON converted to XLSX. Output file:", output_file)
            elif output_ext == '.ods':
                pyexcel.save_as(array=df.values, dest_file_name=output_file)
                print("JSON converted to ODS. Output file:", output_file)
            else:
                print("Invalid output file extension. Please provide a file with the extension '.csv', '.xlsx', or '.ods'.")
        else:
            print("Invalid input file extension. Please provide a file with the extension '.json', '.csv', '.xls', '.xlsx', or '.ods'.")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 json_to_output.py <input_file> <output_file> [to_json]")
        print("Arguments:")
        print("  <input_file>    Path to the input file with the extension '.json', '.csv', '.xls', '.xlsx', or '.ods'.")
        print("  <output_file>   Path to the output file with the extension '.json', '.csv', '.xlsx', or '.ods'.")
        print("  [to_json]       (Optional) Set this flag to convert the input file to JSON.")
        sys.exit(1)
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        to_json = len(sys.argv) > 3 and sys.argv[3].lower() == 'to_json'
        convert_json_to_output(input_file, output_file, to_json)
