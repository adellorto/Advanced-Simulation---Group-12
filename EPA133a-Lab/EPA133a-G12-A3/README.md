# Created by:

**Group Number**: 12

| **Name**             | **Student ID** |
| -------------------- | -------------- |
| Bettin Lorenzo       | 6132928        |
| Dell'Orto Alessandro | 6129161        |
| Le Grand Tangui      | 6172075        |
| Precup Ada           | 5240719        |
| van Engelen Ralph    | 4964748        |

## Project Title: Network Model Generation

## Introduction

This project is part of **EPA133a - Advanced Simulation (Assignment 3)**, expanding on the model generation process from the previous assignment and integrating a multi-modelling approach. The focus is on generating an agent-based simulation model using **Mesa 2.1.4** and overlaying it onto a **NetworkX-based network model**. The simulation explores goods transport over the **N1 and N2 highways in Bangladesh**, incorporating main side roads longer than 25 km.

### The assignment requires:

- **Automatic model generation** from input data (CSV files).
- **Integration of Mesa's agent-based simulation framework** with NetworkX for network representation.
- **Vehicles (trucks) following predefined paths** and shortest routes determined by NetworkX.
- **Experimental scenarios analyzing different levels of bridge failures** and their impact on transport.

The simulation builds on the previous model by adding intersections and two-way traffic, allowing vehicles to dynamically choose routes based on network connectivity.

## How to Use

### 1. Setup Environment

- Install **Python 3.11**.
- Install dependencies using `requirements.txt`.
- Run the simulation using `model_run.py` or visualize it with `model_viz.py`.

### 2. Running Scenarios

- Scenarios define different **bridge breakdown probabilities**.
- The model generates **vehicles at SourceSink locations** every 5 ticks.
- The **shortest path is determined using NetworkX** and stored for future use.
- Experimental results are saved in the `experiment` folder.

### 3. Modifying Inputs

- Modify road data in the `data/` directory (`demo-4.csv`, etc.).
- Adjust bridge conditions and vehicle routing logic in `components.py`.
- Change the seed values to test different simulation conditions.

## Format & Directory Structure

```
EPA133a-G12-A3/ 
│── data/ # Input CSVs (roads, bridges, network data) 
│── experiment/ # Output scenario results and averages over different seeds 
│── img/ # Visualization images 
│── model/ # Core model files & components 
│ ├── components.py # Defines agents (trucks, roads, bridges, intersections) 
│ ├── model.py # Main simulation model 
│ ├── model_run.py # Runs the simulation 
│ ├── model_viz.py # Visualization script 
│── report/ # Analysis of results, including script for plot generation 
│── requirements.txt # Dependencies 
│── README.md # This file
```
For more technical details, refer to individual `README.md` files inside each subfolder.

## Acknowledgments

This assignment is based on **EPA133a - Advanced Simulation** at **TU Delft**, using the **Mesa 2.1.4** framework and **NetworkX**.

For documentation, visit:

- [Mesa Docs](https://mesa.readthedocs.io)
- [Mesa GitHub](https://github.com/projectmesa/mesa)
- [NetworkX Docs](https://networkx.org/)