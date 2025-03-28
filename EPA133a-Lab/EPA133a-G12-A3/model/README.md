Created by:
Yilin HUANG

Continued by Group 12 of EPA133a Advanced Simulation course (2024-2025)

Email:
y.huang@tudelft.nl

Version:
1.2

## Introduction

A simple transport model demo in MESA for EPA133a Advanced Simulation course Assignment 2.

## How to Use

- Create and activate a virtual environment

In PyCharm, you can create a virtual environment by following the steps below:

    1. Open the project in PyCharm
    2. Go to Settings -> Project: epa133a -> Python Interpreter
    3. Click "Add Interpreter"
    4. Select "Add Local Interpreter"
    5. Select Virtualenv Environment
    6. Select New environment
    7. Select Base interpreter as Python 3.11
    8. Click OK and also close the settings with OK

Afterwards, you should see "Python 3.11" (epa133a) in the bottom-right corner of the PyCharm window.
To install the requirements, open a terminal/command line window in PyCharm and type:

```
    $ pip install -r requirements.txt
```

- Launch the simulation model with visualization

```
    $ python model_viz.py
```

- Launch the simulation model without visualization

```
    $ python model_run.py
```

## Files

- [model](...): Contains the model BangladeshModel, which is a subclass of Mesa Model. It reads a csv file (final_input_data.csv) with a specific format for (transport) model generation. The model now uses graph-based shortest path routing with NetworkX, instead of predefined paths. Bridges introduce delay times based on their length, and vehicle movements now include dynamic waiting times for broken infrastructure. The model tracks total delay times for trucks and bridges, and these delays are saved for analysis.

- [components](...): Contains the model component definitions for the (main) model. Includes roads, intersections, sources, sinks, and vehicles. Bridges now have probability-based breakdowns, and delays are dynamically calculated based on bridge length. Vehicles accumulate total delay times and stop if a bridge is broken.

- [model_viz](...): Sets up the visualization; uses the SimpleCanvas element. The visualization now features color-coded infrastructure elements, vehicle count scaling, and updated source/sink indicators. The simulation runs on port 8521 by default.

- [model_run](...): Sets up batch simulations with 10 different seeds and 5 scenarios. Each run tracks average travel times, number of trucks, number of broken bridges, and delays. Bridge delays are stored and averaged across 10 iterations before being saved as bridge_delays_scenario_X.csv.

- [data_pull](...): Contains the data pull routines for the model. The script now includes proximity-based bridge insertion, geographical ordering of sources and sinks, and automatic intersection detection based on road proximity thresholds. The final processed data is saved as final_input_data.csv.

- [ContinuousSpace](ContinuousSpace): The directory contains files needed to visualize Python3 Mesa models on a continuous canvas with geo-coordinates, a functionality not contained in the current Mesa package.

  Editing files in this directory is NOT recommended for our assignment.

- [bonus_data_pull](...): In this file, we define a geospatial data pipeline that merges real-world roads and bridges, calculates approximate intersections using a threshold-based approach, and then uses GeoPandas to compute accurate intersections from the road shapefile. It also handles coordinate reprojection (from EPSG:4326 to UTM Zone 46N) to ensure valid distance measurements. Finally, the file creates visual plots comparing approximate versus accurate intersections, giving a clear view of how the two methods differ.

- [plot_roads](...): This script visualizes the road network and sourcesinks from `final_input_data.csv` using **GeoPandas and Matplotlib**. It reads the data, groups road segments, and plots them with unique colors for each road, while sourcesinks are marked with black 'X' markers. The script ensures correct **geographical ordering of road points**, allows optional **filtering of specific roads**, and includes a **legend and labels** for clarity. Running `python plot_roads.py` generates a **visual representation of the transport network**, useful for verifying data correctness before running the simulation. Users can modify road selection, plotting parameters, or visualization styles as needed.

- [ContinuousSpace/SimpleContinuousModule.py](ContinuousSpace/SimpleContinuousModule.py): Defines `SimpleCanvas`, the Python side of a custom visualization module for drawing objects with continuous positions. This is a slight adaptation of the Flocker example provided by the Mesa project.

  Editing this file is NOT recommended for our assignment.

- [ContinuousSpace/simple_continuous_canvas.js](ContinuousSpace/simple_continuous_canvas.js): JavaScript side of the `SimpleCanvas` visualization module. It takes the output generated by the Python `SimpleCanvas` element and draws it in the browser window via HTML5 canvas. It can draw circles and rectangles. Both can have text annotation. This file is an adaptation of the Flocker example provided by the Mesa project.

  Editing this file is NOT recommended for our assignment


`