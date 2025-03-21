
import numpy as np
import pandas as pd
import requests
import math
import geopandas as gpd
import matplotlib.pyplot as plt
import pyogrio
import os
from shapely.geometry import Point


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


def find_and_insert_intersections(input_data):   #This function finds the intersections between the roads and inserts them in the correct order
                                    # check if it works using the model_viz.py and it the final output file to ensure no intersections are too close to each other
    """
    Identify intersections by finding the closest points between different roads.
    If two objects (links or bridges) are within the threshold distance, an intersection is created.
    """
    intersection_data = []
    processed_intersections = {}  # To track intersection IDs and reuse them across roads

    # Convert lat/lon to numpy arrays for efficient distance calculation
    coords = input_data[['lat', 'lon']].to_numpy()
    roads = input_data['road'].to_numpy()
    ids = input_data['id'].to_numpy()

    # Iterate over each road and compare with all others
    for i, (lat1, lon1, road1, id1) in enumerate(zip(coords[:, 0], coords[:, 1], roads, ids)):  #extracting coordinates from road1
        threshold1 = road_thresholds.get(road1, road_thresholds["default"])  # Get threshold for road1

        for j, (lat2, lon2, road2, id2) in enumerate(zip(coords[:, 0], coords[:, 1], roads, ids)): #extracting coordinates from road2
            if road1 == road2 or i >= j:
                continue  # Skip same road and redundant comparisons

            threshold2 = road_thresholds.get(road2, road_thresholds["default"])  # Get threshold for road2
            distance_threshold = min(threshold1, threshold2)  # Use the higher threshold

            # Calculate distance using haversine function
            distance = haversine(lat1, lon1, lat2, lon2)

            if distance <= distance_threshold:  #check if the two points extractedn are close enough to be considered an intersection
                intersection_key = tuple(sorted([road1, road2]))  # Unique key for the intersection for the pair of roads

                if intersection_key in processed_intersections: #checks if the intersection has already been found in an earlier iteration
                    intersection_id = processed_intersections[intersection_key] # Reuse existing intersection ID if already created for the same pair of roads and avoid duplication
                else:
                    intersection_id = starting_id + len(intersection_data)
                    processed_intersections[intersection_key] = intersection_id

                # Create intersection entries for both roads
                for road, ref_id in [(road1, id1), (road2, id2)]: #storing the id of the objects used as ref_id to insert the intersection so that we can insert the intersection in the correct order
                    intersection = {
                        'road': road,
                        'id': intersection_id,
                        'model_type': 'intersection',
                        'condition': 'N/A',
                        'name': f"Intersection of {road1} and {road2}",
                        'lat': (lat1 + lat2) / 2,  # Midpoint approximation of the location of the intersection
                        'lon': (lon1 + lon2) / 2,
                        'length': 20
                    }
                    intersection_data.append((ref_id, intersection))  # Store with ref_id for correct insertion


    # Insert intersections in the correct order, by comparing the previous id_keys for the objects on the two roads used to find the intersection
    for ref_id, intersection in sorted(intersection_data, key=lambda x: x[0], reverse=True):
        before = input_data[input_data['id'] <= ref_id]
        after = input_data[input_data['id'] > ref_id]
        input_data = pd.concat([before, pd.DataFrame([intersection]), after], ignore_index=True)

    return input_data


# Import raw datasets
clean_roads = pd.read_csv('../data/_roads3.csv')
clean_bridges = pd.read_excel('../data/BMMS_overview.xlsx', engine="openpyxl")

final_input_data = pd.DataFrame(columns=['road', 'id', 'model_type', 'condition', 'name', 'lat', 'lon', 'length'])

starting_id = 1000000
roads_to_process = ['N1', 'N102','N104', 'N105', 'N106', 'N2', 'N204', 'N207', 'N208'] #list of roads to process

#creating the tresholds to find intersections between roads
# creating separate tresholds from the main roads as their coordinates are further away from each other than compared to their side roads.
road_thresholds = {
    "N1": 25, # Threshold for larger roads
    "N2": 25, # Threshold for larger roads
    "default": 15  # Default threshold for smaller roads
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
    starting_id += len(input_data)

    final_input_data = pd.concat([final_input_data, input_data], ignore_index=True)

# Find and insert intersections correctly
final_input_data = find_and_insert_intersections(
    final_input_data)  #finally inserting the intersections into the input data

#since the intersections are added in between the correct obejcts in the file, but with the old id and without updating the rest of the file, we need to update the ids before rendering the final file

# Update IDs to be sequential

# Reassign IDs sequentially after intersections are inserted
final_input_data = final_input_data.sort_values(by=['road', 'lat', 'lon']).reset_index(drop=True)  #ensuring thee file is grouped by rows and ordered by lat and lon
final_input_data['id'] = range(starting_id, starting_id + len(final_input_data)) #updating the ids to be sequential


# Save final updated input data
final_input_data.to_csv('../data/bonus_final_input_data.csv', index=False)









#  BONUS ASSIGNMENT - geospatial analysis
os.environ["SHAPE_RESTORE_SHX"] = "YES" #as the crs is missing, we sets an environment variable telling the underlying file reader (pyogrio) to try to restore or recreate the .shx index file
roads_gdf = gpd.read_file("../data/roads.shp") #read the shapefile
roads_gdf = roads_gdf.set_crs("EPSG:4326") #here we manually assign it a coordinate reference system (CRS). EPSG:4326 corresponds to WGS84, a common geographic coordinate system using latitude and longitude.

# Check and reproject CRS for accurate distance calculations.

if roads_gdf.crs.is_geographic:
   roads_gdf = roads_gdf.to_crs(epsg=32646) #here  we reproject the data to a projected CRS—specifically UTM zone 46N (EPSG:32646), which is suitable for Bangladesh.

# --- Compute Accurate Intersections ---
# We will compute pairwise intersections between road segments.
# For efficiency, we use a spatial index provided by GeoPandas.

accurate_intersections = []  # To store intersection geometries

# Build spatial index for the roads GeoDataFrame
sindex = roads_gdf.sindex

# Iterate over each road segment and check for intersections with others
for idx, road in roads_gdf.iterrows():
    # Get possible intersecting segments using bounding box query
    possible_matches_index = list(sindex.intersection(road.geometry.bounds))
    possible_matches = roads_gdf.iloc[possible_matches_index]

    for jdx, other_road in possible_matches.iterrows():
        # Avoid self-intersection and duplicate comparisons
        if idx >= jdx:
            continue

        # Check if the two geometries intersect
        if road.geometry.intersects(other_road.geometry):
            inter_geom = road.geometry.intersection(other_road.geometry)
            # Depending on the geometry type, extract point(s)
            if inter_geom.geom_type == 'Point':
                accurate_intersections.append(inter_geom)
            elif inter_geom.geom_type in ['MultiPoint', 'GeometryCollection']:
                # Extract points from a multipoint or collection
                for geom in inter_geom.geoms:
                    if geom.geom_type == 'Point':
                        accurate_intersections.append(geom)
            # For line intersections (overlapping segments) we choose a representative point:
            elif inter_geom.geom_type == 'LineString':
                accurate_intersections.append(Point(inter_geom.coords[len(inter_geom.coords)//2]))

# Create a GeoDataFrame for accurate intersections
accurate_intersections_gdf = gpd.GeoDataFrame(geometry=accurate_intersections, crs=roads_gdf.crs)

###############################################################################
# PART 3: COMPARISON OF APPROXIMATE VS. ACCURATE INTERSECTIONS
###############################################################################

# For approximate intersections, we create a GeoDataFrame from the midpoints computed earlier.
# We assume these are stored in final_input_data with model_type == 'intersection'
approx_intersections_df = final_input_data[final_input_data['model_type'] == 'intersection']
approx_intersections_gdf = gpd.GeoDataFrame(
    approx_intersections_df,
    geometry=[Point(xy) for xy in zip(approx_intersections_df['lon'], approx_intersections_df['lat'])],
    crs="EPSG:4326"  # Assuming original data is in geographic coordinates
)

# Reproject approximate intersections to the same CRS as accurate intersections if needed
if approx_intersections_gdf.crs != roads_gdf.crs:
    approx_intersections_gdf = approx_intersections_gdf.to_crs(roads_gdf.crs)

# Visualization
fig, ax = plt.subplots(figsize=(10, 10))

# Plot road geometries
roads_gdf.plot(ax=ax, color='gray', linewidth=0.5, label='Road Segments')

# Plot accurate intersections (in red)
accurate_intersections_gdf.plot(ax=ax, color='red', marker='o', markersize=2, label='Accurate Intersection')

# Plot approximate intersections (in blue)
approx_intersections_gdf.plot(ax=ax, color='blue', marker='x', markersize=50, label='Approximate Intersection')

plt.title("Comparison of Intersection Locations")
plt.legend()
plt.xlabel("Easting")
plt.ylabel("Northing")
plt.show()





# 1) Filter approximate intersections in the region of interest

minx, maxx = 200000, 500000
miny, maxy = 2.5e6, 2.8e6

# 2) Create a new figure
fig, ax = plt.subplots(figsize=(10, 10))

# 3) Plot layers as usual
roads_gdf.plot(ax=ax, color='gray', linewidth=0.5, label='Road Segments')
accurate_intersections_gdf.plot(ax=ax, color='red', marker='o', markersize=3, label='Accurate Intersection')
approx_intersections_gdf.plot(ax=ax, color='blue', marker='x', markersize=70, label='Approximate Intersection')

# 4) Set the plot limits to the bounding box
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

plt.title("Zoomed-In View of Intersections")
plt.legend()
plt.xlabel("Easting")
plt.ylabel("Northing")
plt.show()






