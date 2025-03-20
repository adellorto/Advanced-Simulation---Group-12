import pandas as pd

df = pd.read_csv('../data/final_input_data.csv')

test = df.loc[df['model_type'] == 'intersection',['road', 'id','name']]
print("\n")
roads = df.loc[df['model_type'] == 'intersection','road'].unique()

for road in roads:
    print(road)

print('\n')
test['road1'] = test['name'].str.split().str[-1]
test['road2'] = test['name'].str.split().str[-3]
test['to update'] = test['road']==test['road2']
test.road = test.road.astype(str)
print(test)
print('\n')

for _, road_1 in test.iterrows():
    if not road_1['to update']:
        for index, road_2 in test.iterrows():
            if road_2['to update']:
                if (road_1['road'] == road_2['road1'] and road_1['road2'] == road_2['road']):
                    test.loc[index,'id'] = road_1['id']


print(test)



