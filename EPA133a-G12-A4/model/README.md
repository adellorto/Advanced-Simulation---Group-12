Road file parsing
The RMMS folder provided contains .hml files documenting every road in the network. Notably, files that end in ".traffic"
contain traffic information by vehicle type, totalled in the "AADT" column. This data is the one used to assess
criticality of roads. To access it, we parse through the file using the method in "data_pull".

