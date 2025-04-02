Created by:

|Group Number|12|
|:---:|:-------:|
|Bettin Lorenzo| 6132928|
|Dell'Orto Alessandro| 6129161|
|Le Grand Tangui| 6172075|
|Precup Ada | 5240719 |
|van Engelen Ralph| 4964748|

# Project Title: Network Analysis 
## Introduction

The current directory contains the code for the network analysis of the road network of Bangladesh. The aim of this project is to improve the quality of data obtained about the road network of Bangladesh. Ultimately the details about the road network are to be used to model the transport system of Bangladesh and conclude which arteries or bridges require immediate investments to secure stability in the country. 
The directory contains the following sub-folers:
- `analysis`: contains the final metrics and results of the network analysis
- `data`: contains the raw data and the preprocessed data of the analysis
- `Images`: contains the images used in support of the analysis
- `model`: contains the code necessary to process the raw data and to perform the network analysis
- `Report`: contains the final report of the analysis
- `requirements.txt`: contains all the necessary packages to run the code and can be installed using the command `pip install -r requirements.txt`

## How to Use

Make sure you start of by installing the dependencies, after which you can run the code. The code is divided into two main parts: 
- Road Network Preprocessing: it includes files `bridge_condition_refactored.py`,`data_pull.py`, `data_clean.py`, `road_condition_pull.py`, `road_condition_categories.py`,  `vulnerability_data.py`, `Vulnerability_data_earthquake.py`, `Vulnerability_data_rivererosion`. These files should be ran in this order to ensure the correct preprocessing of the data. 
- Road Network Analysis: it includes files `Criticality_score.py` , `Vulnerability_score.py`. These are the files that should be ran to obtain the final metrics and results of the network analysis.

For further information on the code and the project, please refer to the final report in the `Report` folder as well as to particular README files in the subfolders. 

## Modifying Inputs

You can update the kind of environmental risk you are interested in by changing the vulnerability data in the `data` folder. 
You can also modify the type of metric you want to use to evaluate vulnerability and criticality by changing the code in the `model` folder. 
You can also modify the categorization of road condition in the file `road_condition_categories.py` in the `model` folder. 

## **Acknowledgments**
This assignment is based on **EPA133a - Advanced Simulation** at TU Delft. We would like to thank the course instructors for the guidance and support throughout the project.