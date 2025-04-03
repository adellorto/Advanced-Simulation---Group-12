import pandas as pd
import os
import matplotlib.pyplot as plt

def compute_criticality(df):
    df = df.copy()
    criticality = (df["Traffic"].sum() / df["Length"].sum()) - df["Traffic"].sum() / (df["Length"].sum() - df["Length"])
    criticality = (criticality / criticality.min())
    criticality = criticality * df["Length"] / df["Length"].max()

    return criticality

def compute_vulnerability(df):
    ...

    return df


df = pd.read_csv("../data/processed_data/combined_traffic_clean.csv")

df["Criticality_scores"] = compute_criticality(df)

roads_criticalities = df.groupby("Road")["Criticality_scores"].mean()


print(roads_criticalities.sort_values(ascending=False).head(10))

