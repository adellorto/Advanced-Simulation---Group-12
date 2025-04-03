import os
import pandas as pd
import re

folder_path = "../data/RMMS"  # where the .htm files are
output_path = "../data/processed_data/traffic_entire_road.csv"

traffic_info = []

for filename in os.listdir(folder_path):
    if (filename.startswith("N") or filename.startswith("R")) and filename.endswith("detail.htm"):
        file_path = os.path.join(folder_path, filename)

        road_no = None
        road_name = None
        traffic_value = 0  # Default if not found

        try:
            tables = pd.read_html(file_path, header=None)

            for table in tables:
                # Identify Basic Info table
                if str(table.iloc[0, 0]).strip() == "Basic Info":
                    if table.shape[0] > 2 and table.shape[1] > 1:
                        road_no = table.iloc[1, 1]
                        road_name = table.iloc[2, 1]

                # Identify Traffic & Other Info table
                elif str(table.iloc[0, 0]).strip() == "Traffic & Other Info":
                    for _, row in table.iterrows():
                        key = str(row[0]).strip().lower()
                        if "traffic" in key and "aadt" in key:
                            raw_value = str(row[1])
                            match = re.search(r"\d+", raw_value)
                            if match:
                                traffic_value = int(match.group(0))
                            break

            if road_no and road_name:
                traffic_info.append({
                    "Road No.": road_no,
                    "Road Name": road_name,
                    "Traffic (AADT)": traffic_value
                })
                print(f"IT worked for {filename}: AADT = {traffic_value}")
            else:
                print(f"Issues with️ {filename}: Missing Basic Info")

        except Exception as e:
            print(f"Failed for {filename}: {e}")

# Save results
traffic_df = pd.DataFrame(traffic_info)
traffic_df.to_csv(output_path, index=False)
print(f"\n✅ Saved {len(traffic_df)} rows to '{output_path}'")