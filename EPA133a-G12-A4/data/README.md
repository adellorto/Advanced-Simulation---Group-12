# **Format & Directory Structure**
```
data/
│── bgd_nhr_earthquake_barc/                # Raw data about earthquake risk in Bangladesh determined by geolocation
│── bgd_nhr_floods_barc/                    # Raw data about flooding risk in Bangladesh determined by geolocation
│── bgd_nhr_rivererosion_barc/              # Raw data about river erosion risk in Bangladesh determined by geolocation
│── processed_data/                         # Core model input for the metric calculations
│   ├── average.py    # Defines agents (trucks, roads, bridges)
│   ├── model.py         # Main simulation model
│   ├── model_run.py     # Runs the simulation
│   ├── model_viz.py     # Visualization (if needed)
│── report/              # Final report & analysis of results, including the script which creates the plots present in the report
│── requirements.txt     # Dependencies
│── README.md            # This file