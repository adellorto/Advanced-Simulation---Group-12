Created by:
|Group Number|12|
|:---:|:-------:|
|Bettin Lorenzo| 6132928|
|Dell'Orto Alessandro| 6129161|
|Le Grand Tangui| 6172075|
|Precup Ada | 5240719 |
|van Engelen Ralph| 4964748|

# Project Title: Initial Data Exploration Road Network
## Introduction

The aim of this coding project is to improve the quality of data obtained about the road network of Bangladesh. Ultimately the details about the road network are to be used to model the transport system of Bangladesh and conclude which arteries or bridges require immediate investments to secure stability in the country. In order to ensure that drawn conclusions are valid, this pre-processing steps is critical in securing validity to the ulterior simulation.

## How to Use

Make sure you upload your own version or copy of the data file `road_network.csv` in the DIRECTORY NAMED "DATA\RAW" before running the code. 

It is essential that the data file has the following format:
**Roads File**
- each row should represent one continuous road segment
- column 1 represents the road segment ID
- the following columns repeat over groups of three explaining the name of the first LRP taken form the road, its latitude and its longitude. 

### Bridges File
- `bridges.tsv` should contain bridge information.
- `Roads_InfoAboutEachLRP_1.csv` provides road connectivity data.
- Ensure data is formatted correctly before processing.

#### Expected Format for `bridges.tsv`:
- **Bridge ID**: Unique identifier for each bridge.
- **Bridge Name**: Name of the bridge (standardized format recommended).
- **Latitude**: Geographical latitude of the bridge.
- **Longitude**: Geographical longitude of the bridge.
- **Road Name**: The name of the road the bridge is on.
- **LRP Name**: Linked Reference Point (LRP) for location reference.
- **Other Attributes**: Additional metadata such as construction year, material type, and condition rating (if available).

#### Expected Format for `Roads_InfoAboutEachLRP_1.csv`:
- **Road Segment ID**: Identifier linking to the road network.
- **LRP Name**: Name of the linked reference point.
- **Latitude**: Geographical latitude of the LRP.
- **Longitude**: Geographical longitude of the LRP.


The requirements.txt file is located in the directory "notebook" and contains all the necessary packages to run the code.


The code is divided into two main parts:
- Road Network Preprocessing
- Bridge Preprocessing

Each section contains incremental steps to process the data and improve its quality. Several steps are predefined in the code using functions and applied later on to the dataset, to ensure flexibility of the code by a new user. 

## Output
The final dataset contains only valid and correctly formatted roads and bridges in Bangladesh, ready for further analysis or integration with other geographic datasets. The output ensures:
- Cleaned and structured road network data.
- Properly formatted bridge information.
- Verified connectivity between roads and bridges for accurate transport modeling.
- Corrected outlier LRPs for improved road continuity.
- Application of smoothing techniques to ensure road data accuracy.

## Notes
- Some roads and bridges may have incorrect latitude and longitude values; these are identified and corrected.
- Duplicate entries are counted and removed based on unique identifiers.
- Ensure correct file paths when running the script in different environment