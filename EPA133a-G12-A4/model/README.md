data_pull
The RMMS folder contains .hml files documenting every road in the network. 
Files ending in .traffic specifically contain traffic data by vehicle type, summarized in the "AADT" column.
This data is used to assess road criticality. To access it, we parse the files using the method in data_pull.

The method checks whether a file is a traffic file using "filename.endswith". 
If it is, the tables within the file are read into a pandas dataframe. 
Table 3, which contains the relevant data, is extracted into df_raw, with Row 3 set as the column headers.
The dataframe is then cleaned and formatted for usability.
The processed file is saved as a CSV and combined with previously parsed files to create a consolidated dataset.

data_clean
After this initial processing, further cleaning is performed in data_clean.
A lambda function removes rows where traffic was not measured, and empty rows are dropped.
To facilitate analysis, the Road and Right-Left RL columns are created by splitting Road - RL. 
The dataframe is then reordered and saved as a new CSV file.


bridge criticality = road criticality, bridge length, bridge width
                            +                +             +