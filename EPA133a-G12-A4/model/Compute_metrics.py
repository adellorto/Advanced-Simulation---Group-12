import pandas as pd
import matplotlib.pyplot as plt

def compute_criticality(df):
    df = df.copy()
    # criticality = (df["Traffic"].sum() / df["Length"].sum()) - df["Traffic"].sum() / (df["Length"].sum() - df["Length"])
    # criticality = (criticality / criticality.min())
    # criticality = criticality * df["Length"] / df["Length"].max()

    # Define u(x(t0)) as total network performance (sum of all AADT)
    ux_total = df["Traffic"].sum()

    # Define u(x(t0); xi) as performance without each component (drop its AADT)
    delta_u = ux_total - df["Traffic"]


    # Normalize delta_u by the maximum drop making value between 0 and 1
    normalized_impact = delta_u / delta_u.max()

    # Define Ti as Li / Lmax
    Ti = df["Length"] / df["Length"].max()

    # Final criticality score
    criticality = normalized_impact * Ti


    return criticality

def compute_vulnerability(df):
    ...

    return df


df = pd.read_csv("../data/processed_data/traffic_entire_road.csv")

df["Criticality_scores"] = compute_criticality(df)
print(df)

# Rank the criticality scores
df = df.sort_values(by="Criticality_scores", ascending=False)


# Save the road criticality DataFrame with criticality scores to a new CSV file
output_path = "../analysis/criticality_scores_ranked.csv"
df.to_csv(output_path, index=False)

#Analyse the distribution of criticality scores
df["Criticality_scores"].plot(kind="kde")
plt.show()

#cut top 10 critical roads
top_critical_roads = df.head(10)
top_critical_roads.to_csv("../analysis/top_critical_roads.csv", index=False)




# Export to new file
criticality_path = '../data/processed_data/roads_with_criticality.csv'
df.to_csv(criticality_path, index=False)

# Load datasets
df_roads = pd.read_csv("../data/processed_data/roads_with_criticality.csv")  # Contains 'Road' and 'Criticality'
df_bridges = pd.read_csv("../data/processed_data/brridges_condition_refactored.csv")  # Contains 'Road' and other bridge data

# Ensure column names match
df_bridges = df_bridges.rename(columns={"road": "Road No."})

# Merge to assign each bridge the criticality of its road
df_bridges= df_bridges.merge(df_roads[["Road No.", "Traffic"]], on="Road No.", how="left")

# Save the updated dataset
df_bridges.to_csv("../data/processed_data/bridges_with_traffic.csv", index=False)

def compute_bridge_criticality(df):
    df = df.copy()
    # Define u(x(t0)) as total network performance (sum of all AADT)
    ux_total = df_roads["Traffic"].sum()

    # Define u(x(t0); xi) as performance without each component (drop its AADT)
    delta_u = ux_total - df["Traffic"]

    # Normalize delta_u by the maximum drop making value between 0 and 1
    normalized_impact = delta_u / delta_u.max()

    # Define Ti as Li / Lmax
    Ti = df["length"] / df["length"].max()

    # Final criticality score
    bridge_criticality = normalized_impact * Ti

    return bridge_criticality

df_bridges["Criticality_scores"] = compute_bridge_criticality(df_bridges)

# Save the road criticality DataFrame with criticality scores to a new CSV file
output_path = "../analysis/bridge_criticality_scores_ranked.csv"
df_bridges.to_csv(output_path, index=False)

# Rank the criticality scores
df_bridges = df_bridges.sort_values(by="Criticality_scores", ascending=False)

#Analyse the distribution of criticality scores
df_bridges["Criticality_scores"].plot(kind="kde")
plt.show()

#cut top 10 critical roads
top_critical_bridges = df_bridges.head(10)
#print(top_critical_bridges)
df_bridges.to_csv("../analysis/top_critical_bridges.csv", index=False)