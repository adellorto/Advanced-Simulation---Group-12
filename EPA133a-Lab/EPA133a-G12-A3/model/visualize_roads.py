
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
import numpy as np

def plot_roads(file_name):
    # Read the data into a DataFrame
    data = pd.read_csv(file_name)
    
    # Remove specific roads (if needed)
    # data = data[~data['road'].isin(['N208', 'N105', 'N104'])]
    
    # Group the data by road and create LineString objects
    roads = []
    for road, group in data.groupby('road'):
        # Sort the points by some criterion if necessary (e.g., by latitude or longitude)
        group = group.sort_values(by='lat')
        line = LineString(zip(group['lon'], group['lat']))
        roads.append({'road': road, 'geometry': line})
    
    # Convert the list of roads to a GeoDataFrame
    gdf = gpd.GeoDataFrame(roads, geometry='geometry')
    
    # Plot the GeoDataFrame
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    
    # Generate a colormap with enough unique colors for each road
    num_roads = len(gdf['road'].unique())
    colors = plt.cm.tab20(np.linspace(0, 1, num_roads))  # Use a colormap to generate colors
    
    for i, road in enumerate(gdf['road'].unique()):
        road_data = gdf[gdf['road'] == road]
        road_data.plot(ax=ax, label=road, linewidth=0.5, color=colors[i])  # Assign a unique color to each road
    
    # Plot sourcesinks with a different marker
    sourcesinks = data[data['model_type'] == 'sourcesink']
    plt.scatter(sourcesinks['lon'], sourcesinks['lat'], marker='x', color='black', label='Sourcesinks')
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Road Links and Sourcesinks')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Move legend outside the plot
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()

file_name = '../data/final_input_data.csv'
# Call the function to plot the roads
plot_roads(file_name)