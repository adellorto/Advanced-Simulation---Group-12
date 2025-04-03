import pandas as pd
import os

path = '../data/RMMS/combined_traffic.csv' #Relative path.
traffic_clean_path = '../data/processed_data/combined_traffic_clean.csv'  #Full output path.


def clean_traffic(filename):
    df_traffic = pd.read_csv(filename)

    #Remove rows where any column contains '*' (gets rid of columns where road wasn't measured).
    df_traffic = df_traffic[~df_traffic.apply(lambda row: row.astype(str).str.contains("\*", regex=True).any(), axis=1)]

    #Several rows are completely empty and removed here.
    df_traffic = df_traffic[df_traffic['Name'].notna()]
    df_traffic.rename(columns={'Start location': 'LRP No'}, inplace=True)

    #Further cleaning of columns and reordering.
    df_traffic[['Road', 'RL']] = df_traffic['Link no'].str.split('-', expand=True)
    df_traffic = df_traffic.drop(columns=['Link no'])
    new_order = ['Road', 'RL'] + [col for col in df_traffic.columns if col not in ['Road', 'RL']]
    df_traffic = df_traffic[new_order]


    return df_traffic


df_clean_traffic = clean_traffic(path)
df_clean_traffic.to_csv(traffic_clean_path, index=False)  # Save directly to traffic_clean_path




