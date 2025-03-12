import numpy as np
import pandas as pd
import requests
import math

# ---------------------------------------------------------------
# importing raw data sets
clean_roads = pd.read_csv('../data/_roads3.csv')
clean_bridges = pd.read_excel('../data/BMMS_overview.xlsx', engine="openpyxl")

# initiating dataframe in the right format as described in README.md
input_data = pd.DataFrame(columns=['road', 'id', 'model_type', 'name', 'lat', 'lon', 'length', 'quality_cat'])

# Selecting which row's components we are studying, ensuring that the code is easily applicable to other rows
road_name = 'N1'

# Selecting the road and bridge data for the selected road
road_data = clean_roads[clean_roads['road'] == road_name]
bridge_data = clean_bridges[clean_bridges['road'] == road_name]

# ---------------------------------------------------------------


# ---------------------------------------------------------------
# Updating the model input dataframe with components from roads and turning them into links

# Since the roads data frame also includes bridges, which we will add later from a different dataset, we first eliminate those from the roads data frame

bridge_LRPs = set(bridge_data['LRPName'])  # Convert bridge LRP values into a set for fast lookup

# Filter out rows where 'lrp' exists in bridge_LRPs
road_data = road_data[~road_data['lrp'].isin(bridge_LRPs)]


# We obtain the links by calculating the distance between each pair of LRPs in the road dataset
# The coordinates of each link are the lat and lon information of the starting point of the link
# The length of each link is the distance between the two points, calculated using the haversine function.
# The name of each link comes from the 'name' column of the starting LRP of the link


def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance in meters between two points on Earth."""
    R = 6371000  # Radius of Earth in meters
    # Convert lat/lon from degrees to radians
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


# Calculate the lengths of the links in meters using the haversine formula
lengths = []
for i in range(len(road_data) - 1):
    lat1 = road_data.iloc[i]['lat']
    lon1 = road_data.iloc[i]['lon']
    lat2 = road_data.iloc[i + 1]['lat']
    lon2 = road_data.iloc[i + 1]['lon']
    distance_m = haversine(lat1, lon1, lat2, lon2)
    lengths.append(distance_m)

# Create the DataFrame for road links using the computed lengths in meters
df_links = pd.DataFrame(columns=['road', 'id', 'model_type', 'name', 'lat', 'lon', 'length', 'quality_cat'])
for i in range(len(road_data) - 1):
    df_links.loc[i] = [
        road_name,
        0,
        'link',
        road_data.iloc[i]['name'],
        road_data.iloc[i]['lat'],
        road_data.iloc[i]['lon'],
        lengths[i],
        'Z'
    ]

# Prepare a DataFrame for the final input data
input_data = df_links.copy()


# ---------------------------------------------------------------


# ---------------------------------------------------------------
# Update input dataframe with bridge components
# Make a function that finds the shortest distance between a bridge and a link so that we can find closest LRPs that correspond to the bridges
def find_insertion_index(bridge_row, links_df):
    distances = np.sqrt(
        (links_df['lat'] - bridge_row['lat']) ** 2 +
        (links_df['lon'] - bridge_row['lon']) ** 2
    )
    # Find the index of the closest link
    return distances.idxmin()


# Go through each bridge and insert it in the correct order
# Create a list to hold the new rows with insertion index info
bridge_rows_with_index = []

for idx, bridge in bridge_data.iterrows():
    insertion_idx = find_insertion_index(bridge, input_data)

    # Build a new row for the bridge. Adjust the column names and values
    new_bridge_row = {
        'road': bridge['road'],  # or road_name if they match
        'id': 0,
        'model_type': 'bridge',  #
        'name': bridge['name'] if 'name' in bridge else 'Bridge',
        'lat': bridge['lat'],
        'lon': bridge['lon'],
        'length': bridge['length'] if 'length' in bridge else 0,
        'quality_cat': bridge['condition'] if 'condition' in bridge else 'Z'
    }

    # Append a tuple with the insertion index and the new row
    bridge_rows_with_index.append((insertion_idx, new_bridge_row))

# Sort the list of bridge rows by the insertion index in descending order
# Inserting from the bottom up prevents shifting of the rows that haven't been processed yet.
bridge_rows_with_index.sort(key=lambda x: x[0], reverse=True)

for insertion_idx, new_bridge_row in bridge_rows_with_index:
    # Insert the new bridge row right after the identified link
    before = input_data.iloc[:insertion_idx + 1]
    after = input_data.iloc[insertion_idx + 1:]
    input_data = pd.concat([before, pd.DataFrame([new_bridge_row]), after], ignore_index=True)
# ---------------------------------------------------------------


# ---------------------------------------------------------------

# Final formatting for data input for the Chittagong-Dhaka Route

# Find the last occurrence of "Chittagong" in the 'name' column
chittagong_matches = input_data[input_data['name'].str.contains("Chittagong", na=False, case=False)]

if not chittagong_matches.empty:
    chit_index = chittagong_matches.index.max()  # Get the last occurrence index
    print(f"Last Chittagong LRP found at index: {chit_index}")

    # Keep only the rows up to and including the last Chittagong entry
    input_data_filtered = input_data.iloc[:chit_index + 1].copy()
else:
    print("Warning: No entry containing 'Chittagong' found in the 'name' column.")

# Reverse the dataset so that Chittagong is first (source) and Dhaka is last (sink)
input_data_filtered = input_data_filtered[::-1].reset_index(drop=True)

# --- Update IDs ---
input_data_filtered['id'] = range(1000000, 1000000 + len(input_data_filtered))

# Ensure correct sink and source assignment
input_data_filtered.loc[0, 'model_type'] = 'source'  # First row → "source" (Chittagong)
input_data_filtered.loc[len(input_data_filtered) - 1, 'model_type'] = 'sink'  # Last row → "sink" (Dhaka)

# Set correct names for source and sink so the vizualization is intelligable
input_data_filtered.loc[0, 'name'] = "Chittagong"
input_data_filtered.loc[len(input_data_filtered) - 1, 'name'] = "Dhaka"

# Checking the length of the road
total_length_n1_filt = input_data_filtered["length"].sum() / 1000  # Convert to kilometers

# Print the result
print(f"Total length of road N1 (filtered): {total_length_n1_filt:.2f} kilometers")

# (Optional) Save the final DataFrame for inspection
input_data_filtered.to_csv('../data/final_input_data.csv', index=False)