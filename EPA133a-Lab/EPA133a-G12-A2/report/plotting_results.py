import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the data
file_path = "../experiment/experiment_seed_1234567.csv"
df = pd.read_csv(file_path)

# Convert column names to consistent format (removing leading/trailing spaces if any)
df.columns = df.columns.str.strip()

# Ensure the output directory exists
output_dir = "../img"
os.makedirs(output_dir, exist_ok=True)

# Plot 1: Avg Travel Time vs. Num Broken Bridges
plt.figure(figsize=(8, 5))
plt.plot(df["Num_Broken_Bridges"], df["Avg_Travel_Time"], marker='o', linestyle='-', color='b')
plt.xlabel("Number of Broken Bridges")
plt.ylabel("Average Travel Time (minutes)")
plt.title("Impact of Broken Bridges on Travel Time")
plt.grid(True)
plt.savefig(f"{output_dir}/travel_time_vs_bridges.png")  # Save image
plt.show()

# Plot 2: Num Trucks Arrived vs. Num Broken Bridges
plt.figure(figsize=(8, 5))
plt.plot(df["Num_Broken_Bridges"], df["Num_Trucks"], marker='s', linestyle='-', color='r')
plt.xlabel("Number of Broken Bridges")
plt.ylabel("Number of Trucks Arrived")
plt.title("Impact of Broken Bridges on Truck Arrivals")
plt.grid(True)
plt.savefig(f"{output_dir}/trucks_arrived_vs_bridges.png")  # Save image
plt.show()

print(f"Plots saved in {output_dir}")