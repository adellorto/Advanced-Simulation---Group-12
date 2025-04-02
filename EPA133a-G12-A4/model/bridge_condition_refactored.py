import pandas as pd

# Load the Excel file
df_overview = pd.read_excel('../data/BMMS_overview.xlsx')

# Isolate the relevant columns: road, LRPname, length condition, and roadName
df_selected = df_overview[['road', 'LRPName', 'length', 'condition', 'roadName']]

# Map letter conditions to numeric values: A -> 0, B -> 1, C -> 2, D -> 3
mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
df_selected.loc[:, 'condition'] = df_selected['condition'].map(mapping)
# Save the new DataFrame to a CSV file
df_selected.to_csv('../data/processed_data/brridges_condition_refactored.csv', index=False)

print(df_selected.head())