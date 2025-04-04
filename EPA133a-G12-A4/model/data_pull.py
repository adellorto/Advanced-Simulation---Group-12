import os
import pandas as pd

folder_path = "../data/RMMS"  # Relative path, to be changed if needed.

def parse_traffic():
    combined_dfs = []

    #Loop through files in the folder and process those ending with "traffic.htm".
    for filename in os.listdir(folder_path):
        if filename.endswith("traffic.htm"):
            file_path = os.path.join(folder_path, filename)
            try:
                #Read all tables in the file.
                tables = pd.read_html(file_path, header=None)

                #Table 3 contains the data we want.
                df_raw = tables[3]

                #Use row 3 for the headers in the new dataframe.
                df_raw.columns = df_raw.iloc[3]

                #Drop superfluous rows.
                df = df_raw.drop(index=[0, 1, 2, 3]).reset_index(drop=True)

                #Save to a csv file.
                csv_name = filename.replace(".htm", ".csv")
                df.to_csv(os.path.join(folder_path, csv_name), index=False)

                #Add to a combined list with other parsed roads.
                combined_dfs.append(df)

                #Preview
                print(f"\nProcessed: {filename}")

            #Error handling
            except Exception as e:
                print(f"Could not process {filename}: {e}")

    #Set the combined frame to a csv file which we will use.
    combined_df = pd.concat(combined_dfs, ignore_index=True)
    combined_df.to_csv(os.path.join(folder_path, "combined_traffic.csv"), index=False)
    print("\n Traffic files combined into 'combined_traffic.csv'")


parse_traffic()
