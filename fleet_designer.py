import os
import csv
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES

class FleetDesignerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fleet Designer")
        self.root.geometry("1024x480")  # Adjusted width to accommodate the info panel

        self.search_var = tk.StringVar()

        self.search_entry = tk.Entry(root, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X)

        self.search_button = tk.Button(root, text="Search", command=self.update_search)
        self.search_button.pack()

        self.tree = ttk.Treeview(root)
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.info_panel = tk.Label(root, text="Select an item to see details", anchor="nw", justify="left")
        self.info_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.show_info)

        self.ship_details = {}  # Dictionary to store ship details

        self.populate_tree()

    def populate_tree(self):
        self.root_node = self.tree.insert("", "end", text="FLEETS", open=True)
        fleet_dir = os.path.join("system", "database", "fleet")

        self.fleet_nodes = {}
        self.taskforce_nodes = {}
        self.ship_nodes = {}

        for fleet in os.listdir(fleet_dir):
            if fleet == "AEP" or not fleet.endswith(".csv"):
                continue
            fleet_path = os.path.join(fleet_dir, fleet)

            with open(fleet_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    tag = row[0]  # Assuming TAG is in the 1st column
                    fleet_name = row[9]  # Assuming fleet name is in the 10th column
                    taskforce_name = row[7]  # Assuming taskforce is in the 8th column
                    ship_name = row[1]  # Assuming ship name is in the 2nd column
                    definition = row[2]  # Assuming definition is in the 3rd column
                    hull = row[3]  # Assuming hull is in the 4th column
                    version_name = row[4]  # Assuming version name is in the 5th column
                    pride_of_the_fleet = row[5]  # Assuming pride of the fleet is in the 6th column
                    location = row[6]  # Assuming location is in the 7th column
                    naval_base = row[8]  # Assuming naval base is in the 9th column

                    if tag not in self.fleet_nodes:
                        self.fleet_nodes[tag] = self.tree.insert(self.root_node, "end", text=f"Fleet: {tag}", open=True)

                    if fleet_name not in self.taskforce_nodes:
                        self.taskforce_nodes[fleet_name] = self.tree.insert(self.fleet_nodes[tag], "end", text=f"Taskforce: {fleet_name}", open=True)

                    if taskforce_name not in self.taskforce_nodes:
                        self.taskforce_nodes[taskforce_name] = self.tree.insert(self.taskforce_nodes[fleet_name], "end", text=f"Taskforce: {taskforce_name}", open=True)

                    self.ship_nodes[ship_name] = self.tree.insert(self.taskforce_nodes[taskforce_name], "end", text=ship_name, open=True)

                    # Store ship details
                    self.ship_details[ship_name] = {
                        "definition": definition,
                        "hull": hull,
                        "version_name": version_name,
                        "pride_of_the_fleet": pride_of_the_fleet,
                        "location": location,
                        "naval_base": naval_base
                    }

    def update_search(self):
        search_term = self.search_var.get().lower()
        for ship_name, node in self.ship_nodes.items():
            if search_term in ship_name.lower():
                self.tree.see(node)
                self.tree.selection_set(node)
            else:
                self.tree.selection_remove(node)

    def show_info(self, event):
        selected_item = self.tree.selection()[0]
        item_text = self.tree.item(selected_item, "text")
        item_type = self.get_node_type(selected_item)
        info = f"Type: {item_type}\nName: {item_text}\n"

        if item_type == "fleet":
            taskforces = [self.tree.item(child, "text") for child in self.tree.get_children(selected_item)]
            info += f"Taskforces: {', '.join(taskforces)}"
        elif item_type == "taskforce":
            ships = [self.tree.item(child, "text") for child in self.tree.get_children(selected_item)]
            info += f"Ships: {', '.join(ships)}"
        elif item_type == "ship":
            # Retrieve ship details
            ship_details = self.get_ship_details(item_text)
            info += f"Shipname: {item_text}\n"
            info += f"Definition: {ship_details['definition']}\n"
            info += f"Hull: {ship_details['hull']}\n"
            info += f"Version Name: {ship_details['version_name']}\n"
            info += f"Pride of the Fleet: {ship_details['pride_of_the_fleet']}\n"
            info += f"Location: {ship_details['location']}\n"
            info += f"Naval Base: {ship_details['naval_base']}\n"

        self.info_panel.config(text=info)

    def get_node_type(self, node):
        parent = self.tree.parent(node)
        if parent == "":
            return "root"
        grandparent = self.tree.parent(parent)
        if grandparent == "":
            return "fleet"
        great_grandparent = self.tree.parent(grandparent)
        if great_grandparent == "":
            return "taskforce"
        return "ship"

    def get_ship_details(self, shipname):
        return self.ship_details.get(shipname, {})

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FleetDesignerApp(root)
    root.mainloop()