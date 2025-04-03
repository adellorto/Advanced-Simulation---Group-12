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
