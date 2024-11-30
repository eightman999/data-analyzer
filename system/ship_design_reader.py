import re
import csv
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Display file selection dialog
Tk().withdraw()  # Hide Tkinter main window
input_file = askopenfilename(title="Select input file")

# Get the directory and filename of the selected file
input_dir = os.path.dirname(input_file)
input_filename = os.path.basename(input_file)
output_filename = f"converted_{os.path.splitext(input_filename)[0]}.csv"
output_file = os.path.join('database/design', output_filename)

# List to store results
results = []
module_keys = set()
upgrade_keys = set()

# Initialize flags
inside_modules = False
inside_upgrades = False

# Read lines from the file
with open(input_file, mode='r', encoding='utf-8') as file:
    lines = file.readlines()

# First pass to collect all module and upgrade keys
for line in lines:
    line = line.strip()
    if re.match(r'\s*modules\s*=\s*{', line):
        inside_modules = True
        inside_upgrades = False
        continue
    if re.match(r'\s*upgrades\s*=\s*{', line):
        inside_upgrades = True
        inside_modules = False
        continue
    if inside_modules and "=" in line:
        key = line.split("=")[0].strip()
        module_keys.add(key)
    if inside_upgrades and "=" in line:
        key = line.split("=")[0].strip()
        upgrade_keys.add(key)
    if re.match(r'\s*}', line):
        inside_modules = False
        inside_upgrades = False

# Variables to hold current equipment variant information
current_section = ""
create_equipment_variant = False
inside_upgrades = False
inside_modules = False
name = ""
type_ = ""
name_group = ""
parent_version = ""
modules = {}
upgrades = {}
design_team = ""
obsolete = ""
icon = ""

# Second pass to process each line
for line in lines:
    line = line.strip()

    # Detect the start of a new section
    section_match = re.match(r'^(?!create_equipment_variant|upgrades|modules)(\w+)\s*=\s*{', line)
    if section_match:
        current_section = section_match.group(1)
        create_equipment_variant = False
        inside_upgrades = False
        inside_modules = False
        continue
    # Detect create_equipment_variant block
    if re.match(r'\s*create_equipment_variant\s*=\s*{', line):
        create_equipment_variant = True
        inside_upgrades = False
        inside_modules = False
        name = ""
        type_ = ""
        name_group = ""
        parent_version = ""
        modules = {key: None for key in module_keys}
        upgrades = {key: None for key in upgrade_keys}
        design_team = ""
        obsolete = ""
        icon = ""
        continue

    if create_equipment_variant:
        # Extract name
        name_match = re.match(r'\s*name\s*=\s*"([^"]+)"', line)
        if name_match:
            name = name_match.group(1)
            continue

        # Extract type
        type_match = re.match(r'\s*type\s*=\s*(\w+)', line)
        if type_match:
            type_ = type_match.group(1)
            continue

        # Extract name_group
        name_group_match = re.match(r'\s*name_group\s*=\s*(\w+)', line)
        if name_group_match:
            name_group = name_group_match.group(1)
            continue

        # Extract parent_version
        parent_version_match = re.match(r'\s*parent_version\s*=\s*(\d+)', line)
        if parent_version_match:
            parent_version = parent_version_match.group(1)
            continue

        # Extract design_team
        design_team_match = re.match(r'\s*design_team\s*=\s*mio:([^,]+)', line)
        if design_team_match:
            design_team = design_team_match.group(1)
            continue

        # Extract obsolete
        obsolete_match = re.match(r'\s*obsolete\s*=\s*(\w+)', line)
        if obsolete_match:
            obsolete = obsolete_match.group(1)
            continue

        # Extract icon
        icon_match = re.match(r'\s*icon\s*=\s*(\w+)', line)
        if icon_match:
            icon = icon_match.group(1)
            continue

        # Detect start of upgrades block
        if re.match(r'\s*upgrades\s*=\s*{', line):
            inside_upgrades = True
            inside_modules = False
            continue

        # Process upgrades block
        if inside_upgrades:
            upgrade_pair_match = re.match(r'\s*([^=]+)\s*=\s*(\d+)', line)
            if upgrade_pair_match:
                upgrade_key = upgrade_pair_match.group(1).strip()
                upgrade_value = upgrade_pair_match.group(2).strip()
                upgrades[upgrade_key] = upgrade_value
                continue
            if re.match(r'\s*}', line):
                inside_upgrades = False
                continue

        # Detect start of modules block
        if re.match(r'\s*modules\s*=\s*{', line):
            inside_modules = True
            inside_upgrades = False
            continue

        # Process modules block
        if inside_modules:
            module_pair_match = re.match(r'\s*([a-zA-Z0-9_]+)\s*=\s*([a-zA-Z0-9_]+)', line)
            if module_pair_match:
                module_key = module_pair_match.group(1).strip()
                module_value = module_pair_match.group(2).strip()
                modules[module_key] = module_value
                continue
            if re.match(r'\s*}', line):
                inside_modules = False
                continue

        # End of create_equipment_variant block
        if re.match(r'\s*}', line):
            if create_equipment_variant:
                result = [current_section, name, type_, name_group, parent_version, design_team, obsolete, icon]
                # Ensure all keys are aligned with the header, and upgrades/modules are correctly categorized
                for key in sorted(upgrade_keys):
                    result.append(upgrades.get(key, ""))
                for key in sorted(module_keys):
                    result.append(modules.get(key, ""))
                results.append(result)
            create_equipment_variant = False
            continue

# Write results to CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    header = ['Section', 'name', 'type', 'name_group', 'parent_version', 'design_team', 'obsolete', 'icon'] + sorted(upgrade_keys) + sorted(module_keys)
    writer.writerow(header)
    for result in results:
        writer.writerow(result)

print(f"CSV file created: {output_file}")