
```
model/
│── bridge_condition_refactors.py            # The dataframe that translates `string` bridge conditions to numerical values
│── Compute_metrics.py                       # The main file that runs all the other files and generates the final scores for criticality and vulnerability
│── data_clean.py                            # Raw RMMS data cleaner
│── data_pull.py                             # taking .traffic.htm data from the RMMS folder and parsing it into a dataframe of road sections
│── data_pull_entire road.py                # Taking the average AADT for each road and merging it with length and identification data
│── merging_vulnerability_roads              # Code taht brings together all risk factors for the roads
│── README.md                                # This file
│── road_condition_categories.py             # The dataframe that assigns categories to the condition of the roads,and translates them to numerical values
│── road_condition_pull                      # This file extracts the influencing factorsfor the road condition from .detail.htm files in the RMMS folder 
│── vulnerability_data_earthquake.py         # Assigns the weight of earthquake risk to each road
│── vulnerability_data_floods.py             # Assigns the weight of flood risk to each road
│── vulnerability_data_rivererosion.py       # Assigns the weight of river erosion risk to each road

```
The subfolder `model` is made up of the above mentioned python files. Each file contains code for a subtask of the network analysis, and can be modified independently of the others. 
All outputs from this file, except for the `Compute_metrics`, are saved in the `processed_data` subfolder. The `Compute_metrics` file is the main file that runs all the other files and generates the final output, saved in `analysis`.

## Road file parsing
The RMMS folder contains .htm files documenting every road in the network. 
Files ending in .traffic specifically contain traffic data by vehicle type, per road link, summarized in the "AADT" column. Files ending in .detail contain summaries for the entire road. 
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

