clean_bridges = pd.read_excel('../data/BMMS_overview.xlsx', engine="openpyxl")

#initiating dataframe in the right format as described in README.md
input_data = pd.DataFrame(columns=['road', 'id', 'model_type', 'name', 'lat' , 'lon'   , 'length' , 'quality_cat'])

#Selecting which row's components we are studying, ensuring that the code is easily applicable to other rows
road_name = 'N1'

#Selecting the road and bridge data for the selected road
road_data = clean_roads[clean_roads['road'] == road_name]
bridge_data = clean_bridges[clean_bridges['road'] == road_name]
