import csv
import yaml
import codecs
from tkinter import Tk


# Display file selection dialog for YAML file
Tk().withdraw()  # Hide Tkinter main window
yaml_file = 'countries_l_japanese.yml'

# Read the BOM-encoded UTF-8 YAML file
with codecs.open(yaml_file, 'r', encoding='utf-8-sig') as file:
    yaml_data = yaml.safe_load(file)

# Create an array of tuples to store key-value pairs
key_value_pairs = []

# Populate the array with key-value pairs from the YAML file, ignoring keys that start with 'l_japanese:' or have empty values
for key, value in yaml_data.items():
    if not key.startswith('l_japanese:') and value != {}:
        key_value_pairs.append((f"{key}:", value))

# Print the array of key-value pairs
print(key_value_pairs)

# Read the CSV file to get the list of TAG values, ignoring the first row
csv_file = '00_countries.csv'
tags = []

with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    next(reader)  # Skip the first row
    for row in reader:
        if row['TAG']:  # Check if TAG is not empty
            tags.append(row['TAG'])

# Read the CSV file again and update the JP column, ignoring the first row
updated_rows = []

with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    first_row = next(reader)  # Skip the first row
    updated_rows.append(first_row)  # Add the first row back without changes
    for row in reader:
        tag = row['TAG']
        if tag and tag in yaml_data:  # Check if TAG is not empty and exists in YAML data
            row['JP'] = yaml_data[tag]
        updated_rows.append(row)

# Write the updated content back to the CSV file
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['TAG', '地域', 'JP']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"CSV file updated: {csv_file}")