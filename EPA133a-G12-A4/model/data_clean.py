import pandas as pd
import os

path = '../data/RMMS/combined_traffic.csv'
traffic_clean_path = '../data/processed_data/combined_traffic_clean.csv'  # Full output path


def clean_traffic(filename):
    df_traffic = pd.read_csv(filename)

    # Remove rows where any column contains '*' (gets rid of columns where road wasn't measured)
    df_traffic = df_traffic[~df_traffic.apply(lambda row: row.astype(str).str.contains("\*", regex=True).any(), axis=1)]

    # Keep only rows where 'Name' is not NaN
    df_traffic = df_traffic[df_traffic['Name'].notna()]
    df_traffic.rename(columns={'Start location': 'LRP No'}, inplace=True)

    df_traffic[['Road', 'RL']] = df_traffic['Link no'].str.split('-', expand=True)
    df_traffic = df_traffic.drop(columns=['Link no'])
    new_order = ['Road', 'RL'] + [col for col in df_traffic.columns if col not in ['Road', 'RL']]
    df_traffic = df_traffic[new_order]


    return df_traffic

def clean_lrps(filename):
    df_lrps = pd.read_csv(filename)
    print(df_lrps.head())
    df_lrps = df_lrps.iloc[:, 1:-2]  # Drops first column (index 0) and second-to-last column (-2)
    df_lrps = df_lrps[df_lrps['LRP No'].notna()]
    df_traffic = pd.read_csv(path)
    df_lrps['Road'] = df_traffic['Road']
    return df_lrps

#df_assignment3 = pd.read_csv("../../EPA133a-Lab/EPA133a-G12-A3/data/final_input_data.csv")
#df_assignment3['id'] = df_assignment3['id'].replace("1000", "LRPS")

lrps_path = '../data/RMMS/combined_lrps.csv'
lrps_clean_path = '../data/processed_data/combined_lrps_clean.csv'  # Full output path

df_clean_traffic = clean_traffic(path)
df_clean_traffic.to_csv(traffic_clean_path, index=False)  # Save directly to clean_path

df_clean_lrps = clean_lrps(lrps_path)
df_clean_lrps.to_csv(lrps_clean_path, index=False)



