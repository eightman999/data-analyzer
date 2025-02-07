import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image

def show_turret_data(self):
    tier = self.tier_var.get()
    data = []

    base_dir = os.path.dirname(__file__)
    modules_dir = os.path.abspath(os.path.join(base_dir, '..', 'database', 'modules'))
    for file_name in os.listdir(modules_dir):
        if file_name.endswith('.shm'):
            with open(os.path.join(modules_dir, file_name), 'r', encoding='utf-8') as file:
                try:
                    json_data = json.load(file)
                    if isinstance(json_data, list):
                        for item in json_data:
                            if isinstance(item, dict):
                                if item.get('type') == 'main_gun' and (not tier or item.get('tier') == tier):
                                    data.append(item)
                    elif isinstance(json_data, dict):
                        if json_data.get('type') == 'main_gun' and (not tier or json_data.get('tier') == tier):
                            data.append(json_data)
                    else:
                        messagebox.showwarning("Warning", f"Unexpected data format in {file_name}")
                except json.JSONDecodeError:
                    messagebox.showerror("Error", f"Failed to parse {file_name}")

    if not data:
        messagebox.showinfo("No Data", "No matching data found.")
        return

    dialog = tk.Toplevel(self)
    dialog.title("砲塔データ")
    dialog.geometry("600x400")

    columns = ["name", "tier", "year", "manpower", "description"]
    tree = ttk.Treeview(dialog, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for item in data:
        tree.insert("", "end", values=[
            item.get("name", ""),
            item.get("tier", ""),
            item.get("year", ""),
            item.get("manpower", ""),
            item.get("description", "")
        ])

    def on_select():
        selected_item = tree.selection()[0]
        item_data = tree.item(selected_item, "values")
        selected_data = next(item for item in data if item["name"] == item_data[0])

        xy_dialog = tk.Toplevel(self)
        xy_dialog.title("XY位置決定")
        tk.Label(xy_dialog, text="X位置:").grid(row=0, column=0)
        x_entry = tk.Entry(xy_dialog)
        x_entry.grid(row=0, column=1)
        tk.Label(xy_dialog, text="Y位置:").grid(row=1, column=0)
        y_entry = tk.Entry(xy_dialog)
        y_entry.grid(row=1, column=1)
        tk.Label(xy_dialog, text="角度").grid(row=2, column=0, columnspan=2)
        degree_entry = tk.Entry(xy_dialog)
        degree_entry.grid(row=2, column=1)

        def on_xy_confirm():
            try:
                x = float(x_entry.get())
                y = float(y_entry.get())
                deg = float(degree_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid X or Y position. Please enter numeric values.")
                return
            graphics_image = selected_data.get("graphics", {}).get("image")
            pixel_per_meter = selected_data.get("graphics", {}).get("pixel_per_meter")
            if not graphics_image or not pixel_per_meter:
                messagebox.showerror("Error", "Graphics or scaling data missing in the selected item.")
                return

            try:
                image_file_path = os.path.join(modules_dir, graphics_image)
                with Image.open(image_file_path) as img:
                    original_width, original_height = img.size
                    scaled_width = int(original_width * pixel_per_meter)
                    scaled_height = int(original_height * pixel_per_meter)

                self.armo_images.append({
                    "image_name": graphics_image,
                    "scaled_width": scaled_width,
                    "scaled_height": scaled_height,
                    "position": {"x": x-(scaled_width/2), "y": y-(scaled_height/2)},
                    "angle": deg
                })
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image or scaling: {e}")
                return

            self.details_list.insert(
                "", "end",
                values=(f"x:{x}-y:{y}", selected_data["barrel_mount"], selected_data["weight"], selected_data["manpower"])
            )

            xy_dialog.destroy()
            dialog.destroy()

        tk.Button(xy_dialog, text="決定", command=on_xy_confirm).grid(row=3, column=0, columnspan=2)

    tree.pack(expand=True, fill=tk.BOTH)

    select_button = tk.Button(dialog, text="選択", state=tk.DISABLED, command=on_select)
    select_button.pack(side=tk.BOTTOM, pady=10)

    def on_item_select(event):
        select_button.config(state=tk.NORMAL)

    tree.bind("<<TreeviewSelect>>", on_item_select)