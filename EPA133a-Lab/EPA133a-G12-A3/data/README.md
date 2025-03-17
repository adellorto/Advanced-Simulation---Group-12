# Data for Model Generation of Simple Transport Model Demo in MESA

Created by:
Yilin HUANG

Continued by Group 12 of EPA133a Advanced Simulation course (2024-2025)

Email:
y.huang@tudelft.nl

Version:
1.3

## Introduction

The simple transport model demo, see [../model/model.py](../model/model.py) for EPA133a Advanced Simulation course Assignment 3, takes a `csv` input data file from the `data` directory that specifies the infrastructure model components to be generated. The data format used **by the model** is described here.

## Format

|     Column | Description                                              |
|-----------:|:---------------------------------------------------------|
|       road | On which road does the component belong to               |
|         id | **Unique ID** of the component                           |
| model_type | Type (i.e. class) of the model component to be generated |
|       name | Name of the object                                       |
|        lat | Latitude in Decimal Degrees                              |
|        lon | Longitude in Decimal Degrees                             |
|     length | Length of the object in meters                           |
|  condition | The quality category of the object                       |

The `model_type` column specifies the type of the model component to be generated. The model component types are defined in the `components.py` file. The current types are "sourcesink", "link", "bridge", and "intersection". To add or remove the possible types, modify the `components.py` file.

## Data Files

All data files contained in this directory (except `_roads3.csv`, `roads.shp` and `BMMS_overview.xlsx` ) include the pre-procesed information about the roads and bridges in Bangladesh, and use as input to generate `final_input_data.csv`. The file `final_input_data.csv` is generated in `../model/data_pull.py` and is used for the final model generation and scenario analysis. The file `demo-4.csv`does not contain real data and can simply used for practice with model generation.

The files `_roads3.csv`, `roads.shp` and `BMMS_overview.xlsx` include the raw data from the Bangladesh Bridge Management System (BMMS) and are used to generate the pre-processed data files.