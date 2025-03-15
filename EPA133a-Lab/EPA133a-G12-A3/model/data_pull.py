import numpy as np
import pandas as pd
import requests
import math


def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance in meters between two points on Earth."""
    R = 6371000  # Radius of Earth in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def find_insertion_index(bridge_row, links_df):
    distances = np.sqrt(
        (links_df['lat'] - bridge_row['lat']) ** 2 +
        (links_df['lon'] - bridge_row['lon']) ** 2
    )
    return distances.idxmin()


# Importing raw datasets
clean_roads = pd.read_csv('../data/_roads3.csv')
clean_bridges = pd.read_excel('../data/BMMS_overview.xlsx', engine="openpyxl")

final_input_data = pd.DataFrame(columns=['road', 'id', 'model_type', 'condition', 'name', 'lat', 'lon', 'length'])

starting_id = 1000000
roads_to_process = ['N1','N2','N3'] #Insert list from Lorenzo here

for road_name in roads_to_process:
    road_data = clean_roads[clean_roads['road'] == road_name]
    bridge_data = clean_bridges[clean_bridges['road'] == road_name]

    bridge_LRPs = set(bridge_data['LRPName'])
    road_data = road_data[~road_data['lrp'].isin(bridge_LRPs)]

    lengths = [
        haversine(road_data.iloc[i]['lat'], road_data.iloc[i]['lon'],
                  road_data.iloc[i + 1]['lat'], road_data.iloc[i + 1]['lon'])
        for i in range(len(road_data) - 1)
    ]

    df_links = pd.DataFrame({
        'road': road_name,
        'id': 0,
        'model_type': 'link',
        'condition': 'Z',
        'name': road_data.iloc[:-1]['name'].values,
        'lat': road_data.iloc[:-1]['lat'].values,
        'lon': road_data.iloc[:-1]['lon'].values,
        'length': lengths
    })

    df_links.loc[0, 'model_type'] = 'sourcesink'
    df_links.loc[len(df_links) - 1, 'model_type'] = 'sourcesink'

    input_data = df_links.copy()

    bridge_rows_with_index = []
    for _, bridge in bridge_data.iterrows():
        insertion_idx = find_insertion_index(bridge, input_data)
        new_bridge_row = {
            'road': bridge['road'],
            'id': 0,
            'model_type': 'bridge',
            'condition': bridge.get('condition', 'Z'),
            'name': bridge.get('name', 'Bridge'),
            'lat': bridge['lat'],
            'lon': bridge['lon'],
            'length': bridge.get('length', 0)
        }
        bridge_rows_with_index.append((insertion_idx, new_bridge_row))

    bridge_rows_with_index.sort(key=lambda x: x[0], reverse=True)
    for insertion_idx, new_bridge_row in bridge_rows_with_index:
        before = input_data.iloc[:insertion_idx + 1]
        after = input_data.iloc[insertion_idx + 1:]
        input_data = pd.concat([before, pd.DataFrame([new_bridge_row]), after], ignore_index=True)

    if road_name == 'N1':
        chittagong_matches = input_data[input_data['name'].str.contains("Chittagong", na=False, case=False)]
        if not chittagong_matches.empty:
            chit_index = chittagong_matches.index.max()
            input_data = input_data.iloc[:chit_index + 1].copy()
        input_data = input_data[::-1].reset_index(drop=True)
        input_data.loc[0, 'model_type'] = 'sourcesink'
        input_data.loc[len(input_data) - 1, 'model_type'] = 'sourcesink'
        input_data.loc[0, 'name'] = "Chittagong"
        input_data.loc[len(input_data) - 1, 'name'] = "Dhaka"


    input_data['id'] = range(starting_id, starting_id + len(input_data))
    starting_id += len(input_data)

    final_input_data = pd.concat([final_input_data, input_data], ignore_index=True)

final_input_data.to_csv('../data/final_input_data.csv', index=False)
