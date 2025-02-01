import re
import csv
import os

from utils.actions.select_directory import select_directory

# Function to select directory using a dialog


# Prompt user to select a directory containing equipment files
directory_path = select_directory()
if not directory_path:
    print("No directory selected. Exiting.")
    exit()

# Output file path
output_file_path = os.path.join("utils/database/modules", 'equipment_modules.csv')

# Regular expressions to parse the files
module_pattern = re.compile(r'(\w+)\s*=\s*{')
attribute_pattern = re.compile(r'\b(\w+)\s*=\s*([\w.\-]+)')
stat_pattern = re.compile(r'(\w+)\s*=\s*{([^}]+)}')

# Initialize data structure to hold parsed data
modules_data = []

# Process all files matching "00_S_*.txt" in the selected directory
for filename in os.listdir(directory_path):
    if filename.startswith("00_S_") and filename.endswith(".txt"):
        input_file_path = os.path.join(directory_path, filename)

        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        modules = content.split('}')

        for module in modules:
            match = module_pattern.search(module)
            if not match:
                continue

            module_name = match.group(1)
            module_data = {
                'modulename': module_name,
                'category': '',
                'gfx': '',
                'add_equipment_type': '',
                'manpower': '',
                'critical_parts': '',
                'dismantle_cost_ic': '',
                'steel': '',
                'rubber': '',
                'aluminium': '',
                'chromium': ''
            }

            # Extract attributes like category, gfx, etc.
            for attr_match in attribute_pattern.finditer(module):
                key, value = attr_match.groups()
                if key in module_data:
                    module_data[key] = value

            # Extract complex stats like add_stats, multiply_stats, etc.
            for stat_match in stat_pattern.finditer(module):
                key, stats_content = stat_match.groups()
                stats = re.findall(r'(\w+)\s*=\s*([\w.\-]+)', stats_content)
                if key == 'add_stats':
                    for stat_name, stat_value in stats:
                        module_data[f'add_stats_{stat_name}'] = stat_value
                elif key == 'multiply_stats':
                    for stat_name, stat_value in stats:
                        module_data[f'multiply_stats_{stat_name}'] = stat_value
                elif key == 'add_average_stats':
                    for stat_name, stat_value in stats:
                        module_data[f'add_average_stats_{stat_name}'] = stat_value
                elif key == 'build_cost_resources':
                    for resource, amount in stats:
                        module_data[resource] = amount
                elif key == 'can_convert_from':
                    convert_stats = re.findall(r'(\w+)\s*=\s*([\w.\-]+)', stats_content)
                    module_data['convert_cost_ic'] = '%'.join(f'{k}={v}' for k, v in convert_stats)

            modules_data.append(module_data)

# Write data to CSV
if modules_data:
    fieldnames = list(modules_data[0].keys())
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(modules_data)

    print(f'Data has been successfully written to {output_file_path}')
else:
    print("No data to write.")
