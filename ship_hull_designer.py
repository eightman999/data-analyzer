from sys import meta_path

import system.converter as converter
import tkinter as tk
from tkinter import filedialog
import csv

from system.converter import add_archetype
from system.tools.nakaten_delete import convert_name
from system.tools.declaration import copylight

def select_csv_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV files", "*.csv")],
        defaultextension=".csv"
    )
    return file_path

def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header
        data = []
        for row in reader:
            if row[1] == '-':  # Check if row[1] is '-'
                row[1] = convert_name(row[0],row[16],row[17])  # Convert row[0] and assign to row[1]
            data.append(row)
    return data

def make_ship_hull(data):
    data_for_yml = "l_japanese:\n# Ship hulls\n"
    # data_for_hull = "# Ship hulls\n"
    # data_for_hull = data_for_hull + copylight()
    ship_data = []
    archetype_data = {}

    for row in data[1:]:
        archetype = row[19]
        max_armor = float(row[11]) if row[11] else 0.0
        min_armor = float(row[12]) if row[12] else 0.0
        avg_armor = (max_armor + min_armor) / 2
        HP = converter.hit_and_org_points_converter(
            float(row[2]) if row[2] else 0.0,
            float(row[13]) if row[13] else 0.0,
            float(row[3]) if row[3] else 0.0,
            float(row[4]) if row[4] else 0.0,
            float(row[18]) if row[18] else 0.0,
            avg_armor,
            float(row[14]) if row[14] else 0.0,
            float(row[15]) if row[15] else 0.0
        )
        ORG = converter.org_point_converter(
            float(row[2]) if row[2] else 0.0,
            float(row[13]) if row[13] else 0.0,
            float(row[3]) if row[3] else 0.0,
            float(row[4]) if row[4] else 0.0,
            float(row[18]) if row[18] else 0.0,
            avg_armor,
            float(row[14]) if row[14] else 0.0,
            float(row[15]) if row[15] else 0.0
        )
        COST = converter.ship_cost_generator(
            float(row[2]) if row[2] else 0.0,
            float(row[18]) if row[18] else 0.0,)
        #     avg_armor,
        #     float(row[14]) if row[14] else 0.0,
        #     float(row[13]) if row[13] else 0.0,
        #     row[20]
        # )
        VISIVLE = converter.surface_visibility_converter(
            float(row[3]) if row[3] else 0.0,
            float(row[4]) if row[4] else 0.0,
            float(row[18]) if row[18] else 0.0,
            float(row[9]) if row[9] else 0.0,row[20]
        )
        ship_data.append((row[0], row[1],
                          HP,
                          ORG,
                          COST,
                          VISIVLE
                          ))
        data_for_hull = converter.To_Code(row[1],row[18],archetype,row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],HP,ORG,COST,VISIVLE,row[15])
        if archetype not in archetype_data:
            archetype_data[archetype] = []

        archetype_data[archetype].append(data_for_hull)



    print(ship_data)
    with open('ship_data_output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Sysname', 'HitPoints', 'OrgPoints', 'Cost', 'Visibility'])  # Add appropriate headers
        writer.writerows(ship_data)
    for archetype, hull_data_list in archetype_data.items():
        with open(f'ship_hull_{archetype}.txt', 'w', encoding='utf-8') as f:
            f.write(f"# Archetype: {archetype}\n")
            for hull_data in hull_data_list:
                f.write(hull_data)
                f.write("\n")
    return data

if __name__ == "__main__":
    # Select CSV file
    csv_file_path = select_csv_file()
    print(f"Selected CSV file: {csv_file_path}")

    # Read CSV file
    csv_data = read_csv(csv_file_path)
    make_ship_hull(csv_data)
