import os
import pandas as pd

folder_path = "../data/RMMS"  # Adjust this if needed

def parse_traffic():
    combined_dfs = []

    for filename in os.listdir(folder_path):
        if (filename.startswith("N") or filename.startswith("R")) and filename.endswith("traffic.htm"):
            file_path = os.path.join(folder_path, filename)
            try:
                # Read all tables
                tables = pd.read_html(file_path, header=None)

                # Use Table 3 (includes metadata/data type info)
                df_raw = tables[3]

                # Row 3 has actual headers
                df_raw.columns = df_raw.iloc[3]

                # Drop the first four rows
                df = df_raw.drop(index=[0, 1, 2, 3]).reset_index(drop=True)

                # Optional: Add source file column
                df["source_file"] = filename

                # Save to CSV
                csv_name = filename.replace(".htm", ".csv")
                df.to_csv(os.path.join(folder_path, csv_name), index=False)

                # Add to combined list
                combined_dfs.append(df)

                # Preview
                print(f"\nProcessed: {filename}")
                #print(df.head())

            except Exception as e:
                print(f"Could not process {filename}: {e}")


    combined_df = pd.concat(combined_dfs, ignore_index=True)
    combined_df.to_csv(os.path.join(folder_path, "combined_traffic.csv"), index=False)
    print("\n Traffic files combined into 'combined_traffic.csv'")


def parse_lrps():
    combined_dfs = []

    for filename in os.listdir(folder_path):
        if (filename.startswith("N") or filename.startswith("R")) and filename.endswith("lrps.htm"):
            file_path = os.path.join(folder_path, filename)
            try:
                # Read all tables
                tables = pd.read_html(file_path, header=None)

                # Use Table 3 (includes metadata/data type info)
                df_raw = tables[3]

                # Row 3 has actual headers
                df_raw.columns = df_raw.iloc[3]

                # Drop the first four rows
                df = df_raw.drop(index=[0, 1, 2, 3]).reset_index(drop=True)

                # Optional: Add source file column
                df["source_file"] = filename

                # Save to CSV
                csv_name = filename.replace(".htm", ".csv")
                df.to_csv(os.path.join(folder_path, csv_name), index=False)

                # Add to combined list
                combined_dfs.append(df)

                # Preview
                print(f"\nProcessed: {filename}")
                #print(df.head())

            except Exception as e:
                print(f"Could not process {filename}: {e}")


    combined_df = pd.concat(combined_dfs, ignore_index=True)
    combined_df.to_csv(os.path.join(folder_path, "combined_lrps.csv"), index=False)
    print("\n LRPS files combined into 'combined_lrps.csv'")

parse_traffic()
parse_lrps()

