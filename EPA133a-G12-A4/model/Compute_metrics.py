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


