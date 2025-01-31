import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

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

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.left_frame.pack_propagate(False)

        self.middle_frame = tk.Frame(self.main_frame)
        self.middle_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.middle_frame.pack_propagate(False)

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.right_frame.pack_propagate(False)

        # Add scrollbars to the left frame
        self.left_scrollbar_y = tk.Scrollbar(self.left_frame, orient=tk.VERTICAL)
        self.left_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.left_scrollbar_x = tk.Scrollbar(self.left_frame, orient=tk.HORIZONTAL)
        self.left_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree = ttk.Treeview(self.left_frame, yscrollcommand=self.left_scrollbar_y.set, xscrollcommand=self.left_scrollbar_x.set)
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.left_scrollbar_y.config(command=self.tree.yview)
        self.left_scrollbar_x.config(command=self.tree.xview)

        # Add scrollbars to the middle frame
        self.middle_scrollbar_y = tk.Scrollbar(self.middle_frame, orient=tk.VERTICAL)
        self.middle_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.middle_scrollbar_x = tk.Scrollbar(self.middle_frame, orient=tk.HORIZONTAL)
        self.middle_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.middle_canvas = tk.Canvas(self.middle_frame, yscrollcommand=self.middle_scrollbar_y.set, xscrollcommand=self.middle_scrollbar_x.set)
        self.middle_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.middle_scrollbar_y.config(command=self.middle_canvas.yview)
        self.middle_scrollbar_x.config(command=self.middle_canvas.xview)

        self.info_panel = tk.Frame(self.middle_canvas)
        self.middle_canvas.create_window((0, 0), window=self.info_panel, anchor="nw")
        self.info_panel.bind("<Configure>", lambda e: self.middle_canvas.configure(scrollregion=self.middle_canvas.bbox("all")))

        self.tree.bind("<<TreeviewSelect>>", self.show_info)

        self.ship_details = {}  # Dictionary to store ship details

        self.populate_tree()

        # Add scrollbars to the right frame
        self.right_scrollbar_y = tk.Scrollbar(self.right_frame, orient=tk.VERTICAL)
        self.right_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_scrollbar_x = tk.Scrollbar(self.right_frame, orient=tk.HORIZONTAL)
        self.right_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.right_canvas = tk.Canvas(self.right_frame, yscrollcommand=self.right_scrollbar_y.set, xscrollcommand=self.right_scrollbar_x.set)
        self.right_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.right_scrollbar_y.config(command=self.right_canvas.yview)
        self.right_scrollbar_x.config(command=self.right_canvas.xview)

        self.flags_panel = tk.Frame(self.right_canvas)
        self.right_canvas.create_window((0, 0), window=self.flags_panel, anchor="nw")
        self.flags_panel.bind("<Configure>", lambda e: self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all")))

        self.display_flags_and_countries()  # Always display flags and countries

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

                    tag_id = f"{tag}_tag"
                    fleet_id = f"{tag}_{fleet_name}_fleet"
                    taskforce_id = f"{tag}_{fleet_name}_{taskforce_name}_taskforce"
                    ship_id = f"{tag}_{fleet_name}_{taskforce_name}_{ship_name}_ship"

                    if tag_id not in self.fleet_nodes:
                        self.fleet_nodes[tag_id] = self.tree.insert(self.root_node, "end", text=tag, open=True)

                    if fleet_id not in self.fleet_nodes:
                        self.fleet_nodes[fleet_id] = self.tree.insert(self.fleet_nodes[tag_id], "end", text=fleet_name, open=True)

                    if taskforce_id not in self.taskforce_nodes:
                        self.taskforce_nodes[taskforce_id] = self.tree.insert(self.fleet_nodes[fleet_id], "end", text=taskforce_name, open=True)

                    self.ship_nodes[ship_id] = self.tree.insert(self.taskforce_nodes[taskforce_id], "end", text=ship_name, open=True)

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
        for widget in self.info_panel.winfo_children():
            widget.destroy()

        selected_item = self.tree.selection()[0]
        item_type = self.get_node_type(selected_item)

        if item_type == "root":
            print("Root node selected")
        elif item_type == "fleet":
            print("Fleet node selected")
            self.display_task_forces(selected_item)
        elif item_type == "taskforce":
            print("Taskforce node selected")
            self.display_task_forces(selected_item)
        elif item_type == "ship":
            print("Ship node selected")
            self.display_ships(selected_item)
            self.display_ship_details(self.tree.item(selected_item, "text"))
            self.show_design_button()


    def display_task_forces(self, fleet_node):
        taskforces = [self.tree.item(child, "text") for child in self.tree.get_children(fleet_node)]
        info = f"F/TF:\n {'\n '.join(taskforces)}"
        label = tk.Label(self.info_panel, text=info, anchor="nw", justify="left")
        label.pack(expand=True, fill=tk.BOTH)

    def display_ships(self, taskforce_node):
        ships = [self.tree.item(child, "text") for child in self.tree.get_children(taskforce_node)]
        if not ships:
            return  # Do not display anything if the list is empty
        info = f"Ships:\n {'\n'.join(ships)}"
        label = tk.Label(self.info_panel, text=info, anchor="nw", justify="left")
        label.pack(expand=True, fill=tk.BOTH)

    def display_ship_details(self, ship_name):
        ship_details = self.get_ship_details(ship_name)
        if not ship_details.get('version_name'):
            return  # Do not display anything if 'version_name' is empty
        info = f"Shipname: {ship_name}\n"
        info += f"Definition: {ship_details.get('definition', 'N/A')}\n"
        info += f"Hull: {ship_details.get('hull', 'N/A')}\n"
        info += f"Version Name: {ship_details.get('version_name', 'N/A')}\n"
        info += f"Pride of the Fleet: {ship_details.get('pride_of_the_fleet', 'N/A')}\n"
        info += f"Location: {ship_details.get('location', 'N/A')}\n"
        info += f"Naval Base: {ship_details.get('naval_base', 'N/A')}\n"
        label = tk.Label(self.info_panel, text=info, anchor="nw", justify="left")
        label.pack(expand=True, fill=tk.BOTH)

    def display_flags_and_countries(self, tag=None):
        for widget in self.flags_panel.winfo_children():
            widget.destroy()

        flags_dir = os.path.join("system", "database", "FLAGS")
        country_dir = os.path.join("system", "database", "country_tag")

        # Collect TAGs from FLEETS
        fleet_tags = set()
        fleet_dir = os.path.join("system", "database", "fleet")
        for fleet in os.listdir(fleet_dir):
            if fleet == "AEP" or not fleet.endswith(".csv"):
                continue
            fleet_path = os.path.join(fleet_dir, fleet)
            with open(fleet_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    fleet_tags.add(row[0])  # Assuming TAG is in the 1st column

        flags = [f for f in os.listdir(flags_dir) if f.endswith('.tga') and len(f) == 7 and f[:3] in fleet_tags]
        countries = {}

        for country_file in os.listdir(country_dir):
            if country_file.endswith('.csv'):
                with open(os.path.join(country_dir, country_file), mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header row
                    for row in reader:
                        countries[row[0]] = row[2]  # Map TAG to country name

        for i in range(0, len(flags), 4):
            flag_row = flags[i:i+4]
            flag_images = []
            country_row = []

            for flag in flag_row:
                tag = flag[:3]  # Extract TAG from filename
                if tag in countries:
                    country_row.append(countries[tag])
                else:
                    country_row.append("Unknown")

                img_path = os.path.join(flags_dir, flag)
                img = Image.open(img_path)
                img = img.resize((50, 30), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                flag_images.append((img, tag))

            for j, (img, tag) in enumerate(flag_images):
                label = tk.Label(self.flags_panel, image=img)
                label.image = img  # Keep a reference to avoid garbage collection
                label.grid(row=i//4*2, column=j)
                label.bind("<Button-1>", lambda e, t=tag: self.move_to_tag(t))

            for j, country in enumerate(country_row):
                label = tk.Label(self.flags_panel, text=country)
                label.grid(row=i//4*2+1, column=j)

    def move_to_tag(self, tag):
        tag_id = f"{tag}_tag"
        if tag_id in self.fleet_nodes:
            self.tree.see(self.fleet_nodes[tag_id])
            self.tree.selection_set(self.fleet_nodes[tag_id])

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

    def show_design_button(self):
        if hasattr(self, 'design_button'):
            self.design_button.pack_forget()  # Remove the button if it already exists

        self.design_button = tk.Button(self.root, text="Design", command=self.open_design_window)
        self.design_button.pack(side=tk.RIGHT)

    def open_design_window(self):
        selected_item = self.tree.selection()[0]
        ship_name = self.tree.item(selected_item, "text")
        ship_details = self.get_ship_details(ship_name)
        version_name = ship_details.get('version_name')

        if not version_name:
            return  # Do not proceed if 'version_name' is empty

        design_file = 'utils/database/design/converted__ssw_variants_navy.csv'
        elements = []

        with open(design_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'version_name' in row and row['version_name'] == version_name:
                    # Check if the row has any non-empty elements other than the header
                    if any(value for key, value in row.items() if key != 'version_name' and value):
                        elements.append(row)

        if not elements:
            messagebox.showinfo("No Data", "No design elements found for the selected version.")
            return

        def save_changes():
            # Read the entire CSV file
            with open(design_file, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                all_rows = list(reader)

            # Update only the modified rows based on version_name and Section
            for element in elements:
                for row in all_rows:
                    if row['version_name'] == element['version_name'] and row['Section'] == element['Section']:
                        row.update(element)

            # Write the updated rows back to the CSV file
            with open(design_file, 'w', newline='') as csvfile:
                fieldnames = all_rows[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_rows)

            messagebox.showinfo("Success", "Changes saved successfully.")

        def on_cell_edit(event):
            item = tree.selection()[0]
            col = tree.identify_column(event.x)
            col_index = int(col[1:]) - 1
            entry = tk.Entry(tree)
            entry.place(x=event.x, y=event.y)
            entry.focus()

            def save_edit(event):
                new_value = entry.get()
                tree.set(item, column=col, value=new_value)
                elements[int(item)][columns[col_index]] = new_value
                entry.destroy()

            entry.bind("<Return>", save_edit)
            entry.bind("<FocusOut>", lambda e: entry.destroy())

        design_window = tk.Toplevel(self.root)
        design_window.title(f"{version_name}")

        # Add scrollbars to the Treeview
        tree_scrollbar_y = tk.Scrollbar(design_window, orient=tk.VERTICAL)
        tree_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollbar_x = tk.Scrollbar(design_window, orient=tk.HORIZONTAL)
        tree_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        tree = ttk.Treeview(design_window, yscrollcommand=tree_scrollbar_y.set, xscrollcommand=tree_scrollbar_x.set)
        tree.pack(expand=True, fill=tk.BOTH)
        tree_scrollbar_y.config(command=tree.yview)
        tree_scrollbar_x.config(command=tree.xview)

        # Filter out columns with no elements other than the header and remove the first column
        columns = [col for col in list(elements[0].keys())[1:] if any(row[col] for row in elements if col != 'version_name')]

        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)
            max_width = max(len(str(row[col])) for row in elements) * 10  # Estimate width based on character count
            tree.column(col, width=max_width)

        for i, element in enumerate(elements):
            # Check if the row has any non-empty elements other than the header
            if any(value for key, value in element.items() if key != 'version_name' and value):
                tree.insert("", "end", iid=i, values=[element[col] for col in columns])

        tree.bind("<Double-1>", on_cell_edit)

        save_button = tk.Button(design_window, text="Save", command=save_changes)
        save_button.pack(side=tk.BOTTOM)




if __name__ == "__main__":
    root = tk.Tk()
    app = FleetDesignerApp(root)
    root.mainloop()