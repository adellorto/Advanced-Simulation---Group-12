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


df = pd.read_csv("../data/processed_data/traffic_entire_road.csv")

df["Criticality_scores"] = compute_criticality(df)
# Rank the criticality scores
df = df.sort_values(by="Criticality_scores", ascending=False)

# Save the road criticality DataFrame with criticality scores to a new CSV file
output_path = "../analysis/criticality_scores_ranked.csv"
df.to_csv(output_path, index=False)

#Analyse the distribution of criticality scores
df["Criticality_scores"].plot(kind="kde")
#save to Images
plt.savefig("../Images/criticality_scores_distribution.png", dpi=300)
#plt.show()

#cut top 10 critical roads
top_critical_roads = df.head(10)
top_critical_roads.to_csv("../analysis/top_critical_roads.csv", index=False)

#===========================================================================================
# Export roads with criticality to new file for bridge criticality analysis
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

# Rank the criticality scores
df_bridges = df_bridges.sort_values(by="Criticality_scores", ascending=False)

# Save the road criticality DataFrame with criticality scores to a new CSV file
output_path = "../analysis/bridge_criticality_scores_ranked.csv"
df_bridges.to_csv(output_path, index=False)

#Analyse the distribution of criticality scores
df_bridges["Criticality_scores"].plot(kind="kde")
plt.show()

#cut top 10 critical bridges
top_critical_bridges = df_bridges.head(10)
#print(top_critical_bridges)
top_critical_bridges.to_csv("../analysis/top_critical_bridges.csv", index=False)

#===========================================================================================

#Define the vulnerability function
def compute_vulnerability(df):
    df = df.copy()

    # Ensure numeric columns are filled so that the calculation can happen even for NaN values
    df["Condition Numeric"] = pd.to_numeric(df["Condition Numeric"], errors="coerce").fillna(0)
    df["avg_flood_score"] = pd.to_numeric(df["avg_flood_score"], errors="coerce").fillna(0)
    df["avg_erosion_score"] = pd.to_numeric(df["avg_erosion_score"], errors="coerce").fillna(0)
    df["avg_earthquake_score"] = pd.to_numeric(df["avg_earthquake_score"], errors="coerce").fillna(0)


    # Combine all environmental risks into a single weighted risk score
    combined_risk = df["avg_flood_score"] + df["avg_erosion_score"] + df["avg_earthquake_score"]
    df["Vulnerability"] = df["Condition Numeric"] * combined_risk
    # Normalize the vulnerability scores
    df["Vulnerability"] = df["Vulnerability"] / df["Vulnerability"].max()
    # Rank the vulnerability scores
    df = df.sort_values(by="Vulnerability", ascending=False)


    return df

df= pd.read_csv("../data/processed_data/input_road_vulnerability.csv")

df= compute_vulnerability(df)
print(df) 

#Save the road vulnerability DataFrame with vulnerability scores to a new CSV file
output_path = "../analysis/vulnerability_scores_roads_ranked.csv"

#cut top 10 vulnerable roads
top_vulnerable_roads = df.head(10)
top_vulnerable_roads.to_csv("../analysis/top_vulnerable_roads.csv", index=False)






# Define the vulnerability function for bridges
def compute_bridge_vulnerability(df):
    df = df.copy()

    # Ensure numeric columns are filled so that the calculation can happen even for NaN values
    df["condition"] = pd.to_numeric(df["condition"], errors="coerce").fillna(0)
    df["avg_flood_score"] = pd.to_numeric(df["avg_flood_score"], errors="coerce").fillna(0)
    df["avg_erosion_score"] = pd.to_numeric(df["avg_erosion_score"], errors="coerce").fillna(0)
    df["avg_earthquake_score"] = pd.to_numeric(df["avg_earthquake_score"], errors="coerce").fillna(0)

    # Combine all environmental risks into a single weighted risk score
    combined_risk = df["avg_flood_score"] + df["avg_erosion_score"] + df["avg_earthquake_score"]
    df["Vulnerability"] = df["condition"] * combined_risk

    # Normalize the vulnerability scores
    df["Vulnerability"] = df["Vulnerability"] / df["Vulnerability"].max()

    # Rank the vulnerability scores
    df = df.sort_values(by="Vulnerability", ascending=False)

    return df

# Load the bridge vulnerability scores
bridge_vulnerability_df = pd.read_csv("../data/processed_data/input_bridge_vulnerability.csv")

# Load the bridge condition data
bridge_condition_df = pd.read_csv("../data/processed_data/brridges_condition_refactored.csv")

# Inspect columns to check for duplicates
print("Columns in bridge_condition_df before removing duplicates:")
print(bridge_condition_df.columns)

# Remove duplicate columns
bridge_condition_df = bridge_condition_df.loc[:, ~bridge_condition_df.columns.duplicated()]

# Drop duplicate rows based on 'LRPName' to ensure uniqueness
bridge_condition_df = bridge_condition_df.drop_duplicates(subset="LRPName")

# Drop duplicate columns in the bridge vulnerability DataFrame
bridge_vulnerability_df = bridge_vulnerability_df.loc[:, ~bridge_vulnerability_df.columns.duplicated()]
# Drop duplicate rows based on 'LRPName' to ensure uniqueness
bridge_vulnerability_df = bridge_vulnerability_df.drop_duplicates(subset="LRPName")

# Merge the vulnerability scores with the bridge condition data
merged_bridge_df = bridge_vulnerability_df.merge(bridge_condition_df, on="LRPName", how="left")

# Compute vulnerability for bridges
merged_bridge_df = compute_bridge_vulnerability(merged_bridge_df)

# Save the bridge vulnerability DataFrame with vulnerability scores to a new CSV file
output_path = "../analysis/vulnerability_scores_bridges_ranked.csv"
merged_bridge_df.to_csv(output_path, index=False)

# Cut top 10 vulnerable bridges
top_vulnerable_bridges = merged_bridge_df.head(10)
top_vulnerable_bridges.to_csv("../analysis/top_vulnerable_bridges.csv", index=False)

# Display the results
print(f"The ranked bridge vulnerability scores have been saved to '{output_path}'.")
print("Top 10 vulnerable bridges:")
print(top_vulnerable_bridges)