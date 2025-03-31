import pandas as pd
path = '../data/RMMS/combined_traffic.csv'
def clean(filename):

    df_traffic = pd.read_csv(filename)
    print(df_traffic.head())

clean(path)
