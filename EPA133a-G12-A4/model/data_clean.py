import pandas as pd
import os

path = '../data/RMMS/combined_traffic.csv'
clean_path = '../data/RMMS/processed_data/combined_traffic_clean.csv'  # Full output path


def clean_traffic(filename): #not used for now
    df_traffic = pd.read_csv(filename)
    print(df_traffic.head())

    # Remove rows where any column contains '*' (gets rid of columns where road wasn't measured)
    df_traffic = df_traffic[~df_traffic.apply(lambda row: row.astype(str).str.contains("\*", regex=True).any(), axis=1)]

    # Keep only rows where 'Name' is not NaN
    df_traffic = df_traffic[df_traffic['Name'].notna()]
    df_traffic[['Road', 'RL']] = df_traffic['Link no'].str.split('-', expand=True)
    df_traffic = df_traffic.drop(columns=['Link no'])
    new_order = ['Road', 'RL'] + [col for col in df_traffic.columns if col not in ['Road', 'RL']]
    df_traffic['Start'] = df_traffic[new_order]
    df_traffic = df_traffic[new_order]
    return df_traffic

def clean_lrps(filename):
    df_lrps = pd.read_csv(filename)
    print(df_lrps.head())
    df_lrps = df_lrps.iloc[:, 1:-2]  # Drops first column (index 0) and second-to-last column (-2)

    return df_lrps


df_clean_traffic = clean_traffic(path)
df_clean_lrps = clean_lrps(path)
df_clean_traffic.to_csv(clean_path, index=False)  # Save directly to clean_path
df_clean_lrps.to_csv(clean_path, index=False)

