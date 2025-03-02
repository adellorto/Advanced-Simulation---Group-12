import numpy as np
import pandas as pd
import requests

# ---------------------------------------------------------------
#importing cleaned raw data sets
clean_roads = pd.read_csv('../data/_roads3.csv')
clean_bridges = pd.read_excel('../data/BMMS_overview.xlsx', engine="openpyxl")

#initiating dataframe in the right format as described in README.md
input_data = pd.DataFrame(columns=['road', 'id', 'model_type', 'name', 'lat' , 'lon'   , 'length' , 'quality_cat'])

#Selecting which row's components we are studying, ensuring that the code is easily applicable to other rows
road_name = 'N1'

#Selecting the road and bridge data for the selected road
road_data = clean_roads[clean_roads['road'] == road_name]
bridge_data = clean_bridges[clean_bridges['road'] == road_name]

# ---------------------------------------------------------------



# ---------------------------------------------------------------
#Updating the model dataframe with components from roads & bridges dataset

#The input dataframe for the model needs to extract only links from the roads dataset
#Since the roads data frame also includes bridges, which we will add later from a different dataset, we first eliminate those from the roads data frame

bridge_LRPs = set(bridge_data['LRPName']) # Convert bridge LRP values into a set for fast lookup

# Filter out rows where 'lrp' exists in bridge_LRPs
road_data = road_data[~road_data['lrp'].isin(bridge_LRPs)]

road_data.to_csv('../data/road_data.csv', index=False) #delte later
bridge_data.to_csv('../data/bridge_data.csv', index=False) #delete later


#We obtain these links by calculating the distance between each pair of points in the road dataset
#The coordinates of each link are the lat and lon information of the starting point of the link
#The length of each link is the distance between the two points
#The name of each link comes from the 'name' column of the starting point of the link

lengths = []
for i in range(len(road_data)-1):
    lat1 = road_data.iloc[i]['lat']
    lon1 = road_data.iloc[i]['lon']
    lat2 = road_data.iloc[i+1]['lat']
    lon2 = road_data.iloc[i+1]['lon']
    lengths.append(np.sqrt((lat2-lat1)**2 + (lon2-lon1)**2))

df_links = pd.DataFrame(columns=['road', 'id', 'model_type', 'name', 'lat', 'lon', 'length', 'quality_cat'])


for i in range(len(road_data)-1):
    df_links.loc[i] = [road_name, 0, 'link', road_data.iloc[i]['name'], road_data.iloc[i]['lat'], road_data.iloc[i]['lon'], lengths[i], 'Z']

df_links.to_csv('../data/links.csv', index=False) #delete later

# Append `df_links` to `input_data`
input_data = pd.concat([input_data, df_links], ignore_index=True)

#next needed to append the bridges to the input_data dataframe in the right location, so in between the link where needed. So must find way to idenitfy where brigde fits, maybe based on lat/lon

# ---------------------------------------------------------------



# ---------------------------------------------------------------
#Once all the data is introduced, we create the subsequential IDs and fill the empty names
input_data['id']= pd.Series(range(1000000,1000000+len(input_data)))
# ---------------------------------------------------------------