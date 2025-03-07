import os
import pandas as pd
from model import BangladeshModel

"""
    Run simulation 10 times with predefined seeds
    Store all results in a single file
    Compute and store average values per scenario over the 10 seeds
"""

# Probabilities for different scenarios
probabilities = pd.DataFrame({
    'A': [0, 0, 0, 0, 0, 0, 0, 0.05, 0.1],
    'B': [0, 0, 0, 0, 0, 0.05, 0.1, 0.1, 0.2],
    'C': [0, 0, 0, 0.05, 0.1, 0.1, 0.2, 0.2, 0.4],
    'D': [0, 0.05, 0.1, 0.1, 0.2, 0.2, 0.4, 0.4, 0.8],
    'Z': [0, 0, 0, 0, 0, 0, 0, 0, 0]
})

probabilities.index = [f"Scenario {i}" for i in range(len(probabilities))]

# Run time: 5 x 24 hours; 1 tick = 1 minute
run_length = 7200

# Ensure output directory exists
output_dir = "../experiment"
os.makedirs(output_dir, exist_ok=True)

# Predefined list of seeds
seeds = [1234567, 2345678, 3456789, 4567890, 5678901, 6789012, 7890123, 8901234, 9012345, 1234500]

# Store all results in a single list
all_results = []

# Run the simulation for 10 different seeds
for run_id, seed in enumerate(seeds):
    for scenario in probabilities.index:
        breakdown_probabilities = {key: value / run_length for key, value in probabilities.loc[scenario].items()}
        sim_model = BangladeshModel(seed=seed, breakdown_probabilities=breakdown_probabilities)

        # Run simulation
        for _ in range(run_length):
            sim_model.step()

        # Calculate results
        avg_travel_time = round(pd.Series(sim_model.travel_times).mean(), 2)
        num_trucks_arrived = len(sim_model.travel_times)
        num_broken_bridges = sim_model.broken_bridges

        # Print results
        print(f"\n{scenario} - Seed {seed}: Avg. travel time = {avg_travel_time} minutes")
        print(f"Number of trucks arrived at destination: {num_trucks_arrived}")
        print(f"Number of broken bridges: {num_broken_bridges}")

        # Store results
        all_results.append([seed, scenario, avg_travel_time, num_trucks_arrived, num_broken_bridges])

# Save all results to a single CSV
df = pd.DataFrame(all_results, columns=["Seed", "Scenario", "Avg_Travel_Time", "Num_Trucks", "Num_Broken_Bridges"])
output_file = os.path.join(output_dir, "experiment_results.csv")
df.to_csv(output_file, index=False)
print(f"\nAll results saved to {output_file}")

# Compute average values per scenario for clarity
df_avg = df.groupby("Scenario")[["Avg_Travel_Time", "Num_Trucks", "Num_Broken_Bridges"]].mean().reset_index()

# Save average results to another CSV
output_avg_file = os.path.join(output_dir, "experiment_averages.csv")
df_avg.to_csv(output_avg_file, index=False)
print(f"\nAverage results per scenario saved to {output_avg_file}")
