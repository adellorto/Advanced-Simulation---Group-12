import os
import pandas as pd
from model import BangladeshModel

"""
    Run simulation twice with two different input files (standard and bonus runs)
    Each simulation runs 10 times with predefined seeds
    Store all results in separate files for each input file
    Save scenario-specific results over 10 iterations in separate CSV files
"""

#Add here proper input files (standard and bonus)
input_files = ["../data/demo-4.csv", "../data/demo-4.csv"]

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
run_length = 1000

# Ensure output directory exists
output_dir = "../experiment"
os.makedirs(output_dir, exist_ok=True)

# Predefined list of seeds
seeds = [1234567, 2345678, 3456789, 4567890, 5678901, 6789012, 7890123, 8901234, 9012345, 1234500]

for input_file in input_files:
    BangladeshModel.file_name = input_file
    file_identifier = os.path.basename(input_file).replace(".csv", "")
    bonus_suffix = "_bonus" if "bonus" in file_identifier else ""

    # Store all results in a single list
    all_results = []
    scenario_results = {scenario: [] for scenario in probabilities.index}

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
            avg_delay_time = round(pd.Series(sim_model.delay_times_truck).mean(), 2)

            # Print results
            print(f"\n{scenario} - {file_identifier} - Seed {seed}: Avg. travel time = {avg_travel_time} minutes")
            print(f"Number of trucks arrived at destination: {num_trucks_arrived}")
            print(f"Number of broken bridges: {num_broken_bridges}")
            print(f"Average delay time: {avg_delay_time}")
            print(sim_model.delay_times_bridge)

            # Store results
            result_row = [seed, avg_travel_time, num_trucks_arrived, num_broken_bridges, avg_delay_time]
            all_results.append([seed, scenario, avg_travel_time, num_trucks_arrived, num_broken_bridges, avg_delay_time])
            scenario_results[scenario].append(result_row)

    # Save all results to a single CSV
    df = pd.DataFrame(all_results, columns=["Seed", "Scenario", "Avg_Travel_Time", "Num_Trucks", "Num_Broken_Bridges", "Avg_Delay_Time"])
    output_file = os.path.join(output_dir, f"experiment_results_{file_identifier}{bonus_suffix}.csv")
    df.to_csv(output_file, index=False)
    print(f"\nAll results saved to {output_file}")

    # Save individual scenario results over 10 iterations
    for scenario, data in scenario_results.items():
        scenario_filename = f"scenario{scenario.split(' ')[-1]}{bonus_suffix}.csv"
        scenario_output_path = os.path.join(output_dir, scenario_filename)
        scenario_df = pd.DataFrame(data, columns=["Seed", "Avg_Travel_Time", "Num_Trucks", "Num_Broken_Bridges", "Avg_Delay_Time"])
        scenario_df.to_csv(scenario_output_path, index=False)
        print(f"\nScenario {scenario} results saved to {scenario_output_path}")

