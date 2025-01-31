import os
import pandas as pd
import re

# Directory containing the CSV files
directory = 'database/REAL_SHIP_DATA'

# Check if the directory exists
if not os.path.exists(directory):
    raise FileNotFoundError(f"The directory {directory} does not exist.")

# List to hold dataframes
dfs = []

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        dfs.append(df)

# Concatenate all dataframes
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined dataframe to a new CSV file
combined_df.to_csv('database/REAL_SHIP_DATA/combined_ship_data.csv', index=False)

# Read the CSV file
input_file = 'database/REAL_SHIP_DATA/combined_ship_data.csv'
df = pd.read_csv(input_file)

# Fill null values in the 'Class' column with the value from the 'Ship' column
df['Class'] = df['Class'].fillna(df['Ship'])

# Select the required columns and rename them
df = df[['Class', 'Type', 'Displacement (tons)', 'Country or organization', 'First commissioned']]
df.columns = ['Class', 'Type', 'Displacement', 'Country', 'First commissioned']

# Extract the year from 'First commissioned' column
df['YEAR'] = df['First commissioned'].apply(lambda x: re.search(r'\b(19|18)\d{2}\b', str(x)).group(0) if re.search(r'\b(19|18)\d{2}\b', str(x)) else None)

# Remove duplicate rows based on 'Class', 'Type', 'Displacement', 'Country', and 'YEAR'
df = df.drop_duplicates(subset=['Class', 'Type', 'Displacement', 'Country', 'YEAR'])

# Save the reformatted data to a new CSV file
output_file = 'database/REAL_SHIP_DATA/reformatted_ship_data_with_year.csv'
df.to_csv(output_file, index=False)