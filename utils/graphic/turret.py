import json
import os
import tkinter as tk
import utils as turret_figure
from tkinter import ttk, messagebox


def show_turret_data(self):
    tier = self.tier_var.get()
    data = []

    # .smファイルがあるディレクトリを指定
    modules_dir = 'system/database/modules'
    for file_name in os.listdir(modules_dir):
        if file_name.endswith('.shm'):
            with open(os.path.join(modules_dir, file_name), 'r', encoding='utf-8') as file:
                try:
                    json_data = json.load(file)

                    # データがリストの場合
                    if isinstance(json_data, list):
                        for item in json_data:
                            if isinstance(item, dict):  # 各要素が辞書型であることを確認
                                if item.get('type') == 'main_gun' and (not tier or item.get('tier') == tier):
                                    data.append(item)

                    # データが辞書の場合
                    elif isinstance(json_data, dict):
                        if json_data.get('type') == 'main_gun' and (not tier or json_data.get('tier') == tier):
                            data.append(json_data)

                    # 他の形式の場合は警告を表示
                    else:
                        messagebox.showwarning("Warning", f"Unexpected data format in {file_name}")

                except json.JSONDecodeError:
                    messagebox.showerror("Error", f"Failed to parse {file_name}")

    if not data:
        messagebox.showinfo("No Data", "No matching data found.")
        return

    # データを表示するためのダイアログを作成
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

        # Create a dialog to determine x and y positions
        xy_dialog = tk.Toplevel(self)
        xy_dialog.title("XY位置決定")
        tk.Label(xy_dialog, text="X位置:").grid(row=0, column=0)
        x_entry = tk.Entry(xy_dialog)
        x_entry.grid(row=0, column=1)
        tk.Label(xy_dialog, text="Y位置:").grid(row=1, column=0)
        y_entry = tk.Entry(xy_dialog)
        y_entry.grid(row=1, column=1)

        def on_xy_confirm():
            x = x_entry.get()
            y = y_entry.get()
            # .smファイルのline_graphicを参照
            line_graphics = selected_data.get("line_graphic", [])
            turret_figure.to_data(self,line_graphics,x,y)
            print(self.armocircles)
            print(self.armotrapezoids)
            print(self.armotriangles)
            if x and y:
                self.details_list.insert(
                    "", "end",
                    values=(f"x:{x}-y:{y}", selected_data["barrel_mount"], selected_data["weight"], selected_data["manpower"])
                )

                xy_dialog.destroy()
                dialog.destroy()

        tk.Button(xy_dialog, text="決定", command=on_xy_confirm).grid(row=2, column=0, columnspan=2)
    def on_conf_select():

        pass
    tree.pack(expand=True, fill=tk.BOTH)

    select_button = tk.Button(dialog, text="選択", state=tk.DISABLED,command = on_select)
    select_button.pack(side=tk.BOTTOM, pady=10)
    config_button = tk.Button(dialog, text="設定",state=tk.DISABLED, command=on_conf_select)
    config_button.pack(side=tk.BOTTOM, pady=10)

    def on_item_select(event):
        select_button.config(state=tk.NORMAL)

    tree.bind("<<TreeviewSelect>>", on_item_select)
