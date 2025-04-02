import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


'''
    We categorize the roads from A to D based on the number of contracts and the total length of works. A condition of state 'A' represents the highest level of security for the road, while 'D' represents the lowest level of security.
'''

#Start of by exploring the distribution of the works on the roads
roads_df = pd.read_csv('../data/processed_data/road_condition_summary.csv')
print(roads_df.describe())

#75 % of roads have 0 works going on, so we zoom into the top 25% roads being worked on

# Filter roads with any work at all
worked_roads = roads_df[(roads_df['Number of Contracts'] > 0) | (roads_df['Total Length of Works (Km)'] > 0)]

# Get top 25% of roads with work based on Total Length of Works
threshold_length = worked_roads['Total Length of Works (Km)'].quantile(0.75)
threshold_contracts = worked_roads['Number of Contracts'].quantile(0.75)

top_25_percent = worked_roads[
    (worked_roads['Total Length of Works (Km)'] >= threshold_length) |
    (worked_roads['Number of Contracts'] >= threshold_contracts)
]

print("\n📊 Top 25% of Roads With Works Summary:")
print(top_25_percent.describe())


'''
75% of the roads have 0 contracts and 0 km of works. This means that the majority of the roads are in a good condition. They are the roads assigned category A. 

The rest 25% of the roads are split between categories 'B', 'C', and 'D' based on a deeper look amongst their distribution.

We observe that 50% of the roads being worked upon — ~12.5% of total roads — have max 3 work contracts active and at most 5 km of compromised road. These roads make up category B.

We then observe that 25% of the roads being worked on — ~6.25% of total roads — have max 4 work contracts and at most 22 km of compromised road. These roads make up category C.

The remaining roads are assigned category D.
'''
# Define categorization rules based on distribution

def assign_condition_category(row):
    contracts = row['Number of Contracts']
    length = row['Total Length of Works (Km)']

    if contracts == 0 and length == 0:
        return 'A'
    elif contracts <= 3 and length <= 5:
        return 'B'
    elif contracts <= 4 and length <= 22:
        return 'C'
    else:
        return 'D'

# Assign categories
roads_df['Condition Category'] = roads_df.apply(assign_condition_category, axis=1)

#Assign numbers to categories
# 0 is less vulnerable, 4 is most vulnerable
mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 4}
roads_df['Condition Numeric'] = roads_df['Condition Category'].map(mapping)


#Save categorized roads to a new csv file
roads_df.to_csv('../data/processed_data/road_condition_categorized.csv', index=False)

# Visualize the distribution of number of contracts and total kms being worked alongside assigned category

# Plot histograms

# Plot and save number of contracts distribution
plt.figure(figsize=(8, 5))
sns.histplot(roads_df['Number of Contracts'], bins=30, kde=False)
plt.axvline(0, color='green', linestyle='--', label='Category A')
plt.axvline(3, color='orange', linestyle='--', label='Category B upper bound')
plt.axvline(4, color='red', linestyle='--', label='Category C upper bound')
plt.axvline(roads_df['Number of Contracts'].max(), color='black', linestyle='--', label='Category D range')
plt.title('Distribution of Number of Contracts')
plt.xlabel('Number of Contracts')
plt.ylabel('Count')
plt.legend()
plt.tight_layout()
plt.savefig('../Images/contract_distribution_categories.png', dpi=300)
plt.show()
plt.close()


# Plot and save total length of works distribution
plt.figure(figsize=(8, 5))
sns.histplot(roads_df['Total Length of Works (Km)'], bins=30, kde=False)
plt.axvline(0, color='green', linestyle='--', label='Category A')
plt.axvline(5, color='orange', linestyle='--', label='Category B upper bound')
plt.axvline(22, color='red', linestyle='--', label='Category C upper bound')
plt.axvline(roads_df['Total Length of Works (Km)'].max(), color='black', linestyle='--', label='Category D range')
plt.title('Distribution of Total Length of Works (Km)')
plt.xlabel('Total Length of Works (Km)')
plt.ylabel('Count')
plt.legend()
plt.tight_layout()
plt.savefig('../Images/length_distribution_categories.png', dpi=300)
plt.show()
plt.close()


