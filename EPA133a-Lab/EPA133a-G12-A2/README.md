**Created by:**

| Group Number | 12 |
|:-----------:|:--:|
| **Name** | **Student ID** |
| Bettin Lorenzo | 6132928 |
| Dell'Orto Alessandro | 6129161 |
| Le Grand Tangui | 6172075 |
| Precup Ada | 5240719 |
| van Engelen Ralph | 4964748 |


# Project Title: Building Components for Data-Driven Simulation

## **Introduction**
This project is part of **EPA133a - Advanced Simulation (Assignment 2)**, focusing on data-driven simulation model generation using **Mesa**, an agent-based simulation framework. The goal is to study the effects of bridge maintenance and breakdowns on  transport in Bangladesh. 

The assignment requires:
- **Automatic model generation** from input data (CSV files).
- **Agent-based simulation** of trucks moving along a road network.
- **Bridge conditions affecting delays**, with probability-based breakdowns.
- **Experimental scenarios** analyzing different levels of bridge failures.

The core simulation models truck movement along the N1 highway from **Chittagong to Dhaka**, considering bridge quality categories (A-D) and their impact on travel times.

---

## **How to Use**
### **1. Setup Environment**
1. Install Python 3.11.
2. Install dependencies using `requirements.txt`.
3. Run the simulation using `model_run.py`.

### **2. Running Scenarios**
Scenarios define different breakdown probabilities for bridges. Each scenario runs with a specific **seed value** to introduce controlled randomness. The results are stored in the **experiment folder**, named based on the scenario and seed.

### **3. Modifying Inputs**
- Modify road data in the `data/` directory.
- Adjust bridge conditions in `components.py`.
- Change the seed values to test different simulation conditions.

---

### **3. Modifying Inputs**
- Modify road data in `data/` (`demo-1.csv`, `demo-2.csv`, etc.).
- Adjust bridge conditions in `components.py`.
- Experiment with **different seeds** to test variability.

---

## **Format & Directory Structure**
```
EPA133a-G12-A2/
│── data/                # Input CSVs (roads, bridges, network data)
│── experiment/          # Output scenario results
│── img/                 # Visualization images
│── model/               # Core model files & components
│   ├── components.py    # Defines agents (trucks, roads, bridges)
│   ├── model.py         # Main simulation model
│   ├── model_run.py     # Runs the simulation
│   ├── model_viz.py     # Visualization (if needed)
│── report/              # Final report & analysis
│── requirements.txt     # Dependencies
│── README.md            # This file
```

For more **technical details**, refer to individual `README.md` files inside each subfolder.

---

## **Acknowledgments**
This assignment is based on **EPA133a - Advanced Simulation** at TU Delft, using the **Mesa 2.1.4** framework. 

For Mesa documentation, visit:  
- [Mesa Docs](https://mesa.readthedocs.io/en/stable/mesa.html)  
- [Mesa GitHub](https://github.com/projectmesa/mesa)

---


