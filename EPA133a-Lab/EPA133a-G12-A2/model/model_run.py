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

#run_length = 5 * 24 * 60
probabilities = pd.DataFrame({
    'A':[0,0,0,0,0,0,0,0.05,0.1],
    'B':[0,0,0,0,0,0.05,0.1,0.1,0.2],
    'C':[0,0,0,0.05,0.1,0.1,0.2,0.2,0.4],
    'D':[0,0.05,0.1,0.1,0.2,0.2,0.4,0.4,0.8],
    'Z':[0,0,0,0,0,0,0,0,0]
})

probabilities.index = [f"Scenario {i}" for i in range(len(probabilities))]

# run time 1000 ticks
run_length = 3000

#control sequence of random numbers from here to test sensitivity and applicability of different scenarios
seed = 1234567

for scenario in probabilities.index:
    breakdown_probabilities = {key: value / run_length for key, value in probabilities.loc[scenario].items()}
    sim_model = BangladeshModel(seed=seed,breakdown_probabilities = breakdown_probabilities)

    # Check if the seed is set
    #print("SEED " + str(sim_model._seed))

    # One run per index with given steps
    for i in range(run_length):
        sim_model.step()

    # Calculate average travel time
    avg_travel_time = pd.Series(sim_model.travel_times).mean()
    num_trucks_arrived = len(sim_model.travel_times)

    # Print results
    print(f"\nScenario {scenario} - Seed {seed}: Avg. travel time = {round(avg_travel_time,2)} minutes")
    print(f"Number of trucks arrived at destination: {num_trucks_arrived}")


"""
    Save results to a uniquely named file
"""
# Create directory if it doesn't exist
output_dir = "../experiment"

# Create a unique file name based on scenario number and seed
output_file = f"{output_dir}/scenario_{scenario}_seed_{seed}.csv"

# Create a DataFrame for this run
df = pd.DataFrame([[scenario, seed, avg_travel_time, num_trucks_arrived]],
                  columns=["Scenario", "Seed", "Avg_Travel_Time", "Num_Trucks"])

# Save as a separate file for each scenario
df.to_csv(output_file, index=False)

print(f"\nResults saved to {output_file}")

