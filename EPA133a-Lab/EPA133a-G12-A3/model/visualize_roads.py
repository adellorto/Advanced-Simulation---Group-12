import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

def plot_roads(file_name):
    # Read the data into a DataFrame
    data = pd.read_csv(file_name)
    
    # Remove specific roads
    data = data[~data['road'].isin(['N208', 'N105', 'N104'])]
    
    # Convert the DataFrame to a GeoDataFrame
    geometry = [Point(xy) for xy in zip(data['lon'], data['lat'])]
    gdf = gpd.GeoDataFrame(data, geometry=geometry)
    
    # Plot the GeoDataFrame
    plt.figure(figsize=(10, 10))
    for road in gdf['road'].unique():
        road_data = gdf[gdf['road'] == road]
        road_data.plot(ax=plt.gca(), label=road, linewidth=0.1)  # Set linewidth to 0.1 for even thinner lines
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Roads Plot')
    plt.legend()
    plt.show()

file_name = '../data/final_input_data.csv'
# Call the function to plot the roads
plot_roads(file_name)
# remove n208, n105, n104