import csv
import re
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

# Display directory selection dialog
Tk().withdraw()  # Hide Tkinter main window
input_dir = askdirectory(title="Select input directory")

# List to store results
results = []
add_equipment_production_results = []

# Iterate over files in the selected directory
for input_filename in os.listdir(input_dir):
    if 'navy' in input_filename or 'naval' in input_filename:
        input_file = os.path.join(input_dir, input_filename)
        output_filename = f"converted_{input_filename}.csv"
        output_dir = "database/fleet"
        output_file = os.path.join(output_dir, output_filename)
        add_equipment_production_filename = f"add_equipment_production_{input_filename}.csv"
        add_equipment_production_dir = "database/fleet/AEP"
        add_equipment_production_file = os.path.join(add_equipment_production_dir, add_equipment_production_filename)

        # Create directories if they do not exist
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(add_equipment_production_dir, exist_ok=True)

        # Read lines from the file
        with open(input_file, mode='r', encoding='utf-8') as file:
            lines = file.readlines()

        # Variables to hold current fleet, task force, and ship information
        fleet_name = ""
        naval_base = ""
        task_force_name = ""
        location = ""
        tag = ""
        ship_name = ""
        definition = ""
        pride_of_the_fleet = ""
        hull = ""
        version_name = ""

        # Process each line
        for line in lines:
            if line.strip().startswith('#'):
                continue  # Ignore comment lines

            # Extract fleet name directly under fleet={}
            fleet_match = re.match(r'\s*fleet\s*=\s*{', line)
            if fleet_match:
                fleet_name = ""
                continue

            fleet_name_match = re.match(r'\s*name\s*=\s*"([^"]+)"', line)
            if fleet_name_match and fleet_name == "":
                fleet_name = fleet_name_match.group(1)
                continue

            # Extract naval base
            naval_base_match = re.match(r'\s*naval_base\s*=\s*(\d+)', line)
            if naval_base_match:
                naval_base = naval_base_match.group(1)
                continue

            # Extract task force name directly under task_force={}
            task_force_match = re.match(r'\s*task_force\s*=\s*{', line)
            if task_force_match:
                task_force_name = ""
                location = ""
                continue

            task_force_name_match = re.match(r'\s*name\s*=\s*"([^"]+)"', line)
            if task_force_name_match and task_force_name == "":
                task_force_name = task_force_name_match.group(1)
                continue

            # Extract location within task_force block
            location_match = re.match(r'\s*location\s*=\s*(\d+)', line)
            if location_match:
                location = location_match.group(1)
                continue

            # Extract ship name directly under ship={}
            ship_match = re.match(r'\s*ship\s*=\s*{', line)
            if ship_match:
                ship_name = ""
                definition = ""
                pride_of_the_fleet = ""
                hull = ""
                version_name = ""
                continue

            ship_name_match = re.match(r'\s*name\s*=\s*"([^"]+)"', line)
            if ship_name_match and ship_name == "":
                ship_name = ship_name_match.group(1)
                continue

            # Extract pride_of_the_fleet within ship block
            pride_of_the_fleet_match = re.match(r'\s*pride_of_the_fleet\s*=\s*(\w+)', line)
            if pride_of_the_fleet_match:
                pride_of_the_fleet = pride_of_the_fleet_match.group(1)
                continue

            # Extract definition within ship block
            definition_match = re.match(r'\s*definition\s*=\s*(\w+)', line)
            if definition_match:
                definition = definition_match.group(1)
                continue

            # Extract equipment details within ship block
            equipment_match = re.match(r'\s*equipment\s*=\s*{', line)
            if equipment_match:
                continue

            # Extract hull, owner, and version_name within equipment block
            hull_match = re.match(r'\s*([^=]+)\s*=\s*{', line)
            if hull_match:
                hull = hull_match.group(1).strip()
                continue

            owner_match = re.match(r'\s*owner\s*=\s*(\w+)', line)
            if owner_match:
                tag = owner_match.group(1)
                continue

            version_name_match = re.match(r'\s*version_name\s*=\s*"([^"]+)"', line)
            if version_name_match:
                version_name = version_name_match.group(1)
                results.append([tag, ship_name, definition, hull, version_name, pride_of_the_fleet, location, task_force_name, naval_base, fleet_name])
                continue

            # Extract instant_effect details
            instant_effect_match = re.match(r'\s*instant_effect\s*=\s*{', line)
            if instant_effect_match:
                continue

            add_equipment_production_match = re.match(r'\s*add_equipment_production\s*=\s*{', line)
            if add_equipment_production_match:
                creator = ""
                equipment_type = ""
                version_name = ""
                requested_factories = ""
                progress = ""
                industrial_manufacturer = ""
                continue

            creator_match = re.match(r'\s*creator\s*=\s*"([^"]+)"', line)
            if creator_match:
                creator = creator_match.group(1)
                continue

            equipment_type_match = re.match(r'\s*type\s*=\s*(\w+)', line)
            if equipment_type_match:
                equipment_type = equipment_type_match.group(1)
                continue

            version_name_match = re.match(r'\s*version_name\s*=\s*"([^"]+)"', line)
            if version_name_match:
                version_name = version_name_match.group(1)
                continue

            requested_factories_match = re.match(r'\s*requested_factories\s*=\s*(\d+)', line)
            if requested_factories_match:
                requested_factories = requested_factories_match.group(1)
                continue

            progress_match = re.match(r'\s*progress\s*=\s*([\d.]+)', line)
            if progress_match:
                progress = progress_match.group(1)
                continue

            industrial_manufacturer_match = re.match(r'\s*industrial_manufacturer\s*=\s*([\w:]+)', line)
            if industrial_manufacturer_match:
                industrial_manufacturer = industrial_manufacturer_match.group(1)
                add_equipment_production_results.append([creator, equipment_type, version_name, requested_factories, progress, industrial_manufacturer])
                continue

        # Write results to CSV file
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['TAG', 'shipname', 'definition', 'hull', 'version_name', 'pride_of_the_fleet', 'location', 'task_force_name', 'naval_base', 'fleet_name'])  # Header row
            writer.writerows(results)

        # Write add_equipment_production results to a separate CSV file
        with open(add_equipment_production_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['creator', 'type', 'version_name', 'requested_factories', 'progress', 'industrial_manufacturer'])  # Header row
            writer.writerows(add_equipment_production_results)

print(f"CSV files created in directory: {input_dir}")