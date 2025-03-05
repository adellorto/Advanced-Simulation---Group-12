import os
import pandas as pd
from model import BangladeshModel

"""
    Run simulation
    Print output at terminal
    Save results in individual file
"""

# ---------------------------------------------------------------
"""
    Choose your own runtime
"""



probabilities = pd.DataFrame({
    'A':[0,0,0,0,0,0,0,0.05,0.1],
    'B':[0,0,0,0,0,0.05,0.1,0.1,0.2],
    'C':[0,0,0,0.05,0.1,0.1,0.2,0.2,0.4],
    'D':[0,0.05,0.1,0.1,0.2,0.2,0.4,0.4,0.8],
    'Z':[0,0,0,0,0,0,0,0,0]
})

probabilities.index = [f"Scenario {i}" for i in range(len(probabilities))]

#run time 5 x 24 hours; 1 tick 1 minute
run_length = 7200

#control sequence of random numbers from here to test sensitivity and applicability of different scenarios
seed = 1234567

#List for storing results
results = []

# Ensure output directory exists
output_dir = "../experiment"
os.makedirs(output_dir, exist_ok=True)

for scenario in probabilities.index:
    breakdown_probabilities = {key: value / run_length for key, value in probabilities.loc[scenario].items()}
    sim_model = BangladeshModel(seed=seed,breakdown_probabilities = breakdown_probabilities)

    # One run per index with given steps
    for i in range(run_length):
        sim_model.step()

    # Calculate average travel time
    avg_travel_time = round(pd.Series(sim_model.travel_times).mean(),2)
    num_trucks_arrived = len(sim_model.travel_times)
    num_broken_bridges = sim_model.broken_bridges

    # Print results
    print(f"\n{scenario} - Seed {seed}: Avg. travel time = {avg_travel_time} minutes")
    print(f"Number of trucks arrived at destination: {num_trucks_arrived}")
    print(f"Number of broken bridges: {num_broken_bridges}")

    #Store results
    results.append([scenario, avg_travel_time, num_trucks_arrived, num_broken_bridges])


"""
    Save results to a uniquely named file
"""
# Convert results to DataFrame
df = pd.DataFrame(results, columns=["Scenario", "Avg_Travel_Time", "Num_Trucks", "Num_Broken_Bridges"])

# Save results to CSV
output_file = os.path.join(output_dir, f"experiment_seed_{seed}.csv")
df.to_csv(output_file, index=False)

print(f"\nResults saved to {output_file}")

