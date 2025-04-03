
```
model/
│── bridge_condition_refactors.py            # Raw data about earthquake risk in Bangladesh determined by geolocation
│── Compute_metrics.py                       # Raw data about flooding risk in Bangladesh determined by geolocation
│── data_clean.py                            # Raw data about river erosion risk in Bangladesh determined by geolocation
│── data_pull.py                             # Core model input for the metric calculations
│── README.md                                # This file
│── road_condition_categories.py             # Raw road and bridge data inclduing traffic data including `htm` files from which the data is extracted about different attributes of the roads and bridges
│── road_condition_pull                      # Extracted sumamry data for network components
│── vulnerability_data.py                    # Cleaned summary data just for the roads
│── vulnerability_data_earthquake.py         # `shapefile`  containing the geolocation of the earthquake risk in Bangladesh
│── vulnerability_data_rivererosion.py       # the spatial index file that accompanies a shapefile (.shp)
│── README.md                                # 
```
The subfolder `model` is made up of the above mentioned python files. Each file contains code for a subtask of the network analysis, and can be modified independently of the others. 
All outputs from this file, except for the `Compute_metrics`, are saved in the `processed_data` subfolder. The `Compute_metrics` file is the main file that runs all the other files and generates the final output, saved in `analysis`.

Road file parsing
The RMMS folder contains .hml files documenting every road in the network. 
Files ending in .traffic specifically contain traffic data by vehicle type, summarized in the "AADT" column.
This data is used to assess road criticality. To access it, we parse the files using the method in data_pull.

The method checks whether a file is a traffic file using "filename.endswith". 
If it is, the tables within the file are read into a pandas dataframe. 
Table 3, which contains the relevant data, is extracted into df_raw, with Row 3 set as the column headers.
The dataframe is then cleaned and formatted for usability.
The processed file is saved as a CSV and combined with previously parsed files to create a consolidated dataset.

After this initial processing, further cleaning is performed in data_clean.
A lambda function removes rows where traffic was not measured, and empty rows are dropped.
To facilitate analysis, the Road and Right-Left RL columns are created by splitting Road - RL. 
The dataframe is then reordered and saved as a new CSV file.

