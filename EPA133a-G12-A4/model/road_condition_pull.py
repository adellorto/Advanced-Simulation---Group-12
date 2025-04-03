import os
import pandas as pd
from bs4 import BeautifulSoup

# Path to your roadSign files
directory_path = '../data/RMMS'

# Running through a single file of interest to identify the structure

''' 
   We pull the data of interest for determining the condition of a road. this data takes into consideration the number of contracts and the total length of works.
'''

for filename in os.listdir(directory_path):
    if filename.endswith('N1.detail.htm'):
        print(f"\n--- Analyzing: {filename} ---")
        file_path = os.path.join(directory_path, filename)
        try:
            tables = pd.read_html(file_path, header=0)
            print(f"Found {len(tables)} tables.\n")
            for i, table in enumerate(tables):
                print(f"Table {i + 1} Columns: {table.columns.tolist()}")
        except Exception as e:
            print(f"Could not read tables from {filename}: {e}")
        break

'''
    The construction work information is in Table 8, columns 'No. of contracts' ~ [Ongoing work.1] and 'Total length of works (Km) ~ [Ongoing work.2]'
    We now run through Table 8 of each .detail.htm file in RMMS to extract and compile the data into a single DataFrame.
'''
# List to collect data
road_condition_data = []


for filename in os.listdir(directory_path):
    if filename.endswith('.detail.htm'):
        #Isolate one road file to work with
        road_name = filename.replace('.detail.htm', '')
        file_path = os.path.join(directory_path, filename)

        #Initialize fallback variables in case the table is not found, or it's empty
        contracts = 0
        length_km = 0

        try:
            tables = pd.read_html(file_path, header=0)
            if len(tables) >= 8:
                df = tables[7]
                df.dropna(how='all', inplace=True) # Drop rows where all values are NaN
                df.dropna(axis=1, how='all', inplace=True) # Drop columns where all values are NaN

                if df.shape[0] > 3:
                    contracts = pd.to_numeric(df.iloc[3, 1], errors='coerce') #if a value cannot be converted to a number, force pandas to continue and not give an error
                    length_km = pd.to_numeric(df.iloc[3, 2], errors='coerce')

        except Exception as e:
            print(f"Failed to parse {filename}: {e}")

        # This now runs regardless of success or failure and adds a value for each road
        road_condition_data.append({
            'road': road_name,
            'Number of Contracts': contracts if pd.notnull(contracts) else 0,
            'Total Length of Works (Km)': length_km if pd.notnull(length_km) else 0
        })


# Create a DataFrame from the collected data

# Save to CSV with working contracts
output_path = os.path.join('../data/processed_data', 'road_condition_summary.csv')
roads_df = pd.DataFrame(road_condition_data)
roads_df.to_csv(output_path, index=False)


