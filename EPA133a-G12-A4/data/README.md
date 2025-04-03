# **Format & Directory Structure**
```
data/
│── bgd_nhr_earthquake_barc/                # Raw data about earthquake risk in Bangladesh determined by geolocation
│── bgd_nhr_floods_barc/                    # Raw data about flooding risk in Bangladesh determined by geolocation
│── bgd_nhr_rivererosion_barc/              # Raw data about river erosion risk in Bangladesh determined by geolocation
│── processed_data/                         # Core model input for the metric calculations
│   ├── average_erosion_score_per_road.csv                        # The dataframe assignings the weight of erosion risk to each road
│   ├── bridge_flood_scores.csv                                   # The dataframe assignings the weight of flood risk to each bridge
│   ├── bridge_condition_refactored.csv                           # The dataframe that translates `string` bridge conditions to numerical values
│   ├── combined_lrps_clean.csv                                   # ??????????
│   ├── combined_traffic_clean.csv                                # Cleaned traffic data per link including AADT for roads and bridges
│   ├── road_condition_categorized.csv                            # The dataframe that assigns `string` categories to the condition of the roads,and translates them to numerical values
│   ├── road_condition_summary.csv                                # The dataframe summarizes the amount of works and kilometers of damage for each road and can be used as input to modify the condition categorization of roads
│   ├── road_flood_scores.csv                                     # The dataframe assignings the weight for flood risk to each road
│   ├── roads_with_earthquake_vulnerability.csv                   # The dataframe assignings the weight for earthquake risk to each road
│── RMMS/                                  # Raw road and bridge data inclduing traffic data including `htm` files from which the data is extracted about different attributes of the roads and bridges
│── _overview.xls                          # Extracted sumamry data for network components
│── _roads3.csv                            # Cleaned summary data just for the roads
│── bgd_nhr_earthquake_sparsso.shp         # `shapefile`  containing the geolocation of the earthquake risk in Bangladesh
│── bgd_nhr_earthquake_sparsso.shx         # the spatial index file that accompanies a shapefile (.shp)
│── README.md                              # This file
```

All data sets outside of the `processed_data` subfolder are extracted from online sources and is not processed. Citations for data origin can be found in the `Report` folder. 

```