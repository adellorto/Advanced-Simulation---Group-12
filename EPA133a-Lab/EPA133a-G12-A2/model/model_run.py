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
#run time 5 x 24 hours; 1 tick 1 minute
scenario_number = 0
run_length = 5 * 24 * 60

# run time 1000 ticks
# run_length = 1000

#control sequence of random numbers from here to test sensitivity and aplicability of different scenarios
seed = 1234567

sim_model = BangladeshModel(seed=seed)

# Check if the seed is set
print("SEED " + str(sim_model._seed))

# One run per index with given steps
for i in range(run_length):
    sim_model.step()

# Calculate average travel time
avg_travel_time = pd.Series(sim_model.travel_times).mean()
num_trucks_arrived = len(sim_model.travel_times)

# Print results
print(f"Scenario {scenario_number} - Seed {seed}: Avg. travel time = {avg_travel_time}")
print(f"Number of trucks arrived at destination: {num_trucks_arrived}")


"""
    Save results to a uniquely named file
"""
# Create directory if it doesn't exist
output_dir = "../experiment"

# Create a unique file name based on scenario number and seed
output_file = f"{output_dir}/scenario_{scenario_number}_seed_{seed}.csv"

# Create a DataFrame for this run
df = pd.DataFrame([[scenario_number, seed, avg_travel_time, num_trucks_arrived]],
                  columns=["Scenario", "Seed", "Avg_Travel_Time", "Num_Trucks"])

# Save as a separate file for each scenario
df.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")

