import numpy as np
import pandas as pd
import requests
import math

"""
The first section of the data collector centralises the needed procssing functions in one place.
"""

def haversine(lat1, lon1, lat2, lon2): # This function calculates the distance between two points on the earth in meters
    """Calculate the great-circle distance in meters between two points on Earth."""
    R = 6371000  # Radius of Earth in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def find_insertion_index(bridge_row, links_df):  #This function finds the index of the link that is closest to the bridge to ensure that the bridge is inserted in the correct order
    """" Store the information that will help insert the bridges in geographical order between the links """

    distances = np.sqrt(
        (links_df['lat'] - bridge_row['lat']) ** 2 +
        (links_df['lon'] - bridge_row['lon']) ** 2
    )
    return distances.idxmin()

def remove_misplaced_objects(input_data):

    start_end = 0
    roads = input_data['road'].unique()
    print(roads)

    for road in roads:
        for index, row in input_data.loc[input_data['road'] == road].iterrows():
            if row['model_type'] == 'sourcesink':
                start_end = start_end + 1
            elif start_end == 0:
                input_data.iloc[[index,index+1]] = input_data.iloc[[index+1,index]].values
            elif start_end == 2:
                input_data.iloc[[index-1,index]] = input_data.iloc[[index,index-1]].values
        start_end = 0

    """
    for road in roads:
        for index, row in input_data.loc[input_data['road'] == road].iterrows():
            if start_end == 0 and row['model_type'] == 'sourcesink':
                input_data = pd.concat([input_data.loc[index], input_data.drop(index)])
                start_end = start_end + 1
            elif start_end == 1:
                input_data = pd.concat([input_data.drop(index), input_data.loc[index]])
        start_end = 0
    """

    return input_data


def assign_intersection_ids(input_data):
    """
    Ensures intersections with the same last word in the name and road get the same ID.
    The first encountered intersection ID is assigned to the second one.

    Parameters:
        df (pd.DataFrame): DataFrame with columns ['road', 'id', 'model_type', 'name']

    Returns:
        pd.DataFrame: Updated DataFrame with consistent intersection IDs.
    """

    input_data['id'] = range(starting_id, starting_id + len(input_data))  # updating the ids to be sequential

    intersections = input_data.loc[input_data['model_type'] == 'intersection',['road', 'id','name']]

    intersections['road1'] = intersections['name'].str.split().str[-1]
    intersections['road2'] = intersections['name'].str.split().str[-3]
    intersections['to update'] = intersections['road'] == intersections['road2']

    for _, road_1 in intersections.iterrows():
        if not road_1['to update']:
            for index, road_2 in intersections.iterrows():
                if road_2['to update']:
                    if (road_1['road'] == road_2['road1'] and road_1['road2'] == road_2['road']):
                        input_data.loc[index, 'id'] = road_1['id']

    return input_data  # Return updated DataFrame while preserving original order


def find_and_insert_intersections(input_data):   #This function finds the intersections between the roads and inserts them in the correct order
                                    # check if it works using the model_viz.py and it the final output file to ensure no intersections are too close to each other
    """
    Identify intersections by finding the closest points between different roads.
    If two objects (links or bridges) are within the threshold distance, an intersection is created.
    """

    intersection_data = []

    # Convert lat/lon to numpy arrays for efficient distance calculation
    coords = input_data[['lat', 'lon']].to_numpy()
    roads = input_data['road'].to_numpy()
    ids = input_data['id'].to_numpy()

    # Store already detected intersections
    existing_intersections = set()

    # Iterate over each road and compare with all others
    for i, (lat1, lon1, road1, id1) in enumerate(zip(coords[:, 0], coords[:, 1], roads, ids)):
        threshold1 = road_thresholds.get(road1, road_thresholds["default"])  # Get threshold for road1

        for j, (lat2, lon2, road2, id2) in enumerate(zip(coords[:, 0], coords[:, 1], roads, ids)):
            if road1 == road2 or i >= j:
                continue  # Skip same road and redundant comparisons

            threshold2 = road_thresholds.get(road2, road_thresholds["default"])  # Get threshold for road2
            distance_threshold = min(threshold1, threshold2)  # Use the smaller threshold

            # Calculate distance using haversine function
            distance = haversine(lat1, lon1, lat2, lon2)

            if distance <= distance_threshold:  # Check if they should be considered an intersection
                road_pair = (min(road1, road2), max(road1, road2))  # Normalize ordering

                if road_pair in existing_intersections:
                    continue  # Skip if intersection already exists

                # Mark this road pair as having an intersection
                existing_intersections.add(road_pair)

                # Generate a unique intersection ID
                intersection_id = starting_id + len(intersection_data)

                # Create intersection entries for both roads
                for road, ref_id in [(road1, id1), (road2, id2)]:
                    intersection = {
                        'road': road,
                        'id': intersection_id,
                        'model_type': 'intersection',
                        'condition': 'N/A',
                        'name': f"Intersection of {road1} and {road2}",
                        'lat': (lat1 + lat2) / 2,  # Midpoint approximation
                        'lon': (lon1 + lon2) / 2,
                        'length': 20
                    }
                    intersection_data.append((ref_id, intersection))  # Store with ref_id


# Insert intersections in the correct order, by comparing the previous id_keys for the objects on the two roads used to find the intersection
    for ref_id, intersection in sorted(intersection_data, key=lambda x: x[0], reverse=True):
        before = input_data[input_data['id'] <= ref_id]
        after = input_data[input_data['id'] > ref_id]
        input_data = pd.concat([before, pd.DataFrame([intersection]), after], ignore_index=True)

    # Reassign IDs sequentially after intersections are inserted
    input_data = input_data.sort_values(by=['road', 'lat', 'lon']).reset_index(drop=True)  # ensuring the file is grouped by rows and ordered by lat and lon
    input_data = remove_misplaced_objects(input_data)
    input_data = assign_intersection_ids(input_data)

    return input_data


# Import raw datasets
clean_roads = pd.read_csv('../data/_roads3.csv')
clean_bridges = pd.read_excel('../data/BMMS_overview.xlsx', engine="openpyxl")

final_input_data = pd.DataFrame(columns=['road', 'id', 'model_type', 'condition', 'name', 'lat', 'lon', 'length'])

starting_id = 1000000
#roads_to_process = ['N1', 'N102', 'N105', 'N2'] #list of roads to process
#roads_to_process = ['N1', 'N102', 'N105', 'N106', 'N2', 'N204', 'N207', 'N208'] #list of roads to process
roads_to_process = ['N1', 'N102', 'N105', 'N2', 'N204', 'N207', 'N208'] #list of roads to process
# Generate the list of all roads to process for the visualization
#roads_to_process = ['N1', 'N101', 'N102', 'N103', 'N104', 'N105', 'N106', 'N107', 'N108', 'N109', 'N110', 'N111', 'N112', 'N119', 'N120', 'N123', 'N128', 'N129', 'N2', 'N204', 'N205', 'N206', 'N207', 'N208', 'N209', 'N210'] #list of roads to process
#creating the tresholds to find intersections between roads
# creating separate tresholds from the main roads as their coordinates are further away from each other than compared to their side roads.
road_thresholds = {
    "N1": 45, # Threshold for larger roads
    "N2": 45, # Threshold for larger roads
    "default": 45  # Default threshold for smaller roads
}

for road_name in roads_to_process:
    road_data = clean_roads[clean_roads['road'] == road_name]
    bridge_data = clean_bridges[clean_bridges['road'] == road_name]

    bridge_LRPs = set(bridge_data['LRPName']) # Set for faster lookups
    road_data = road_data[~road_data['lrp'].isin(bridge_LRPs)] #eliminateing the bridges from the road data to avoid duplication when inserting the bridges

    lengths = [
        haversine(road_data.iloc[i]['lat'], road_data.iloc[i]['lon'],
                  road_data.iloc[i + 1]['lat'], road_data.iloc[i + 1]['lon'])
        for i in range(len(road_data) - 1)
    ] #in meters

    df_links = pd.DataFrame({
        'road': road_name,
        'id': 0,
        'model_type': 'link',
        'condition': 'Z',
        'name': road_data.iloc[:-1]['name'].values,
        'lat': road_data.iloc[:-1]['lat'].values,
        'lon': road_data.iloc[:-1]['lon'].values,
        'length': lengths
    })          #creating a dataframe with the links in the correct format

    df_links.loc[0, 'model_type'] = 'sourcesink' #setting the first and last link to sourcesink ensuring vehicles can enter and exit the road
    df_links.loc[len(df_links) - 1, 'model_type'] = 'sourcesink'

    input_data = df_links.copy() #append road data to input data

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
        } #initiating the bridge data in the correct format
        bridge_rows_with_index.append((insertion_idx, new_bridge_row)) #storing the bridge data with the index of the link closest to the bridge

    bridge_rows_with_index.sort(key=lambda x: x[0], reverse=True)
    for insertion_idx, new_bridge_row in bridge_rows_with_index: #integrating the bridge data into the input data at the correct location
        before = input_data.iloc[:insertion_idx + 1]
        after = input_data.iloc[insertion_idx + 1:]
        input_data = pd.concat([before, pd.DataFrame([new_bridge_row]), after], ignore_index=True)

    input_data['id'] = range(starting_id, starting_id + len(input_data)) #adding the unique ids to the input data

    final_input_data = pd.concat([final_input_data, input_data], ignore_index=True)

# Find and insert intersections correctly
final_input_data = find_and_insert_intersections(
    final_input_data)  #finally inserting the intersections into the input data

#since the intersections are added in between the correct obejcts in the file, but with the old id and without updating the rest of the file, we need to update the ids before rendering the final file


print(final_input_data.loc[final_input_data['model_type'] == 'intersection', ['id','road','name']])


# Save final updated input data
final_input_data.to_csv('../data/final_input_data.csv', index=False)