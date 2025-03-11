from model import BangladeshModel

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 5 * 24 * 60

# run time 1000 ticks
# run_length = 1000

seed = 1234567

breakdown_probabilities = {
    'A' : 0.8,
    'B' : 0.1,
    'C' : 0.1,
    'D' : 0.1,
    'Z' : 0
}

sim_model = BangladeshModel(seed=seed, breakdown_probabilities=breakdown_probabilities)

# Check if the seed is set
print("SEED " + str(sim_model._seed))

# One run with given steps
for i in range(run_length):
    sim_model.step()

print("\n")
print(sim_model.broken_bridges)
print("\n")
print(len(sim_model.travel_times))