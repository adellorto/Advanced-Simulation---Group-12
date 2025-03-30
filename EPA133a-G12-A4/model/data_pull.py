from bs4 import BeautifulSoup
import pandas as pd

# Specify the file path
file_path = '../data/RMMS/N2.traffic.htm'

# Open and read the HTML file
with open(file_path, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Find all tables in the HTML
tables = soup.find_all('table')

# Check if tables are found
if tables:
    # Parse the first table (or iterate through all tables if needed)
    table = tables[0]
    rows = table.find_all('tr')

    # Extract headers
    headers = [header.text.strip() for header in rows[0].find_all('th')]

    # Extract rows
    data = []
    for row in rows[1:]:
        cells = row.find_all(['td', 'th'])
        data.append([cell.text.strip() for cell in cells])

    # Create a DataFrame
    df = pd.DataFrame(data, columns=headers)
    print(df.head())