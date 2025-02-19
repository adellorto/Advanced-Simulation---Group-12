Created by:
|Group Number|12|
|:---:|:-------:|
|Bettin Lorenzo| Student Number|
|Dell'Orto Alessandro| Student Number|
|Le Grand Tangui| Student Number|
|Precup Ada | 5240719 |
|van Engelen Ralph| Student Number|

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

**Bridges File**

Complete by Ralph


The requirements.txt file is located in the directory "notebook" and contains all the necessary packages to run the code.


The code is divided into two main parts:
- Road Network Preprocessing
- Bridge Preprocessing

Each section contains incremental steps to process the data and improve its quality. Several steps are predefined in the code using functions and applied later on to the dataset, to ensure flexibility of the code by a new user.  