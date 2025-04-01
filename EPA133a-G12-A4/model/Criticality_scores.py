import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("../data/RMMS/processed_data/combined_traffic_clean.csv")

df['length'] = np.random.randint(1, 11, size=len(df))

df["Criticality_scores"] = (df["Traffic"].sum()/df["length"].sum()) - df["Traffic"].sum()/(df["length"].sum()-df["length"])
df["Criticality_scores"] = (df["Criticality_scores"] / df["Criticality_scores"].min()).round(2)

print(df["Criticality_scores"].unique())

df["Criticality_scores"].plot(kind="hist")

plt.show()