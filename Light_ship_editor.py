import tkinter as tk
from tkinter import ttk, simpledialog
from pdx_tools.pdx_ssw import ship_types, role_types

from utils.actions.status_converter import armor_thickness_converter
from utils.actions.export_ship_file import export_ship_str_build, export_ship_file

ship = {
    "開発年": "",
    "国家": "",
    "艦型名": "",
    "艦種": "",
    "全長": "",
    "全幅": "",
    "最高速度": "",
    "巡航速度": "",
    "航続距離": "",
    "燃料量": "",
    "装甲": {},
    "砲塔": {},
    "魚雷": {},
    "対潜装備": {},
    "電装": {},
    "ミサイル": {},
    "機関": {}
}

# メインウィンドウの作成
root = tk.Tk()
root.title("軍艦エディタ")
root.geometry("1280x720")  # 1280x720に設定

# PanedWindowを使って左右に分割
paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

# 左側フレーム
left_frame = ttk.Frame(paned_window, padding=10)
paned_window.add(left_frame, weight=3)

# 右側フレーム
right_frame = ttk.Frame(paned_window, padding=10)
paned_window.add(right_frame, weight=1)

# 左側のラベルとエントリの配置
labels = [
    ("開発年", "国家"),
    ("艦型名", "級"),
    ("全長", "全幅"),
    ("最高速度", "巡航速度"),
    ("航続距離", "燃料量"),
]

entries = {}

# 項目を左フレームに配置
for i, (label1, label2) in enumerate(labels):
    ttk.Label(left_frame, text=label1).grid(row=i, column=0, sticky=tk.W, pady=2)
    entry1 = ttk.Entry(left_frame)
    entry1.grid(row=i, column=1, padx=5, pady=2, sticky=tk.EW)
    entries[label1] = entry1

    if label2:  # 第二のラベルが存在する場合
        ttk.Label(left_frame, text=label2).grid(row=i, column=2, sticky=tk.W, pady=2)
        # 「級」の横をプルダウンに変更
        if label2 == "級":
            combo = ttk.Combobox(left_frame)
            combo['values'] = ship_types
            combo.grid(row=i, column=3, padx=5, pady=2, sticky=tk.EW)
            entries[label2] = combo
        else:
            entry2 = ttk.Entry(left_frame)
            entry2.grid(row=i, column=3, padx=5, pady=2, sticky=tk.EW)
            entries[label2] = entry2

# 左フレームの列幅を調整
left_frame.columnconfigure(1, weight=1)
left_frame.columnconfigure(3, weight=1)


def add_armor():
    # 新しいウィンドウを作成
    armor_window = tk.Toplevel(root)
    armor_window.title("装甲の追加")
    armor_window.geometry("400x200")

    # ダイアログのメインフレーム
    frame = ttk.Frame(armor_window, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)

    # 名前欄
    ttk.Label(frame, text="名前:").grid(row=0, column=0, sticky=tk.W, pady=5)
    armor_name_entry = ttk.Entry(frame, width=25)
    armor_name_entry.grid(row=0, column=1, padx=5, pady=5)

    # 装甲種類プルダウン
    ttk.Label(frame, text="装甲種類:").grid(row=1, column=0, sticky=tk.W, pady=5)
    armor_type_combo = ttk.Combobox(
        frame,
        values=["cupper_nickel", "wooden", "HV_armor_steel",
                "KC_armor_steel", "VC_armor_steel",
                "VH_armor_steel", "CNC_armor_steel",
                "NC_armor_steel", "DU_armor"],
        state="readonly",
        width=22
    )
    armor_type_combo.grid(row=1, column=1, padx=5, pady=5)

    # 装甲圧エントリ
    ttk.Label(frame, text="装甲圧(max-min):").grid(row=2, column=0, sticky=tk.W, pady=5)
    armor_thickness_entry = ttk.Entry(frame, width=25)
    armor_thickness_entry.grid(row=2, column=1, padx=5, pady=5)

    # 部位プルダウン
    ttk.Label(frame, text="部位:").grid(row=3, column=0, sticky=tk.W, pady=5)
    armor_section_combo = ttk.Combobox(frame, values=["艦首", "艦中央部", "艦尾", "甲板", "舷側"], state="readonly",
                                       width=22)
    armor_section_combo.grid(row=3, column=1, padx=5, pady=5)

    # OKボタンとキャンセルボタン
    def submit_armor():
        armor_name = armor_name_entry.get()
        armor_type = armor_type_combo.get()
        armor_thickness = armor_thickness_entry.get()
        armor_section = armor_section_combo.get()

        if armor_name and armor_type and armor_thickness and armor_section:
            try:
                # 入力された装甲圧を分割し、数値型に変換
                max_armor_thickness, min_armor_thickness = map(float, armor_thickness.split("-"))
                armor_stat,Atype = armor_thickness_converter(max_armor_thickness, min_armor_thickness, armor_type)

                # データを辞書に格納
                ship["装甲"][armor_name] = {
                    "A_Name": armor_name,
                    "A_Type": armor_type,
                    "MXT": str(max_armor_thickness),
                    "MIT": str(min_armor_thickness),
                    "PART": str(armor_section),
                    "A_VALU": str(armor_stat),
                }
                equip_listbox.insert(
                    tk.END,
                    f"{armor_name} ({armor_type}, {max_armor_thickness}mm,{min_armor_thickness}mm ,{armor_section})"
                )
                print(f"装甲「{armor_name}」を追加: {ship['装甲'][armor_name]}")
            except ValueError:
                # 数値に変換できない場合のエラーハンドリング
                print("装甲圧には正しい数値を入力してください（例: '50-30'）")
        else:
            print("すべての項目を入力してください")
        armor_window.destroy()


    ttk.Button(frame, text="OK", command=submit_armor).grid(row=4, column=0, columnspan=1, pady=10)
    ttk.Button(frame, text="キャンセル", command=armor_window.destroy).grid(row=4, column=1, columnspan=1, pady=10)



def add_turret():
    # 砲塔を追加するためのダイアログ
    turret_type = simpledialog.askstring("砲塔の追加", "追加する砲塔の種類を入力してください：")
    if turret_type:
        print(f"砲塔「{turret_type}」を追加しました")


def add_torpedo():
    # 魚雷を追加するためのダイアログ
    torpedo_type = simpledialog.askstring("魚雷の追加", "追加する魚雷の種類を入力してください：")
    if torpedo_type:
        print(f"魚雷「{torpedo_type}」を追加しました")


def add_asw():
    # 対潜装備を追加するためのダイアログ
    asw_type = simpledialog.askstring("対潜装備の追加", "追加する対潜装備の種類を入力してください：")
    if asw_type:
        print(f"対潜装備「{asw_type}」を追加しました")


def add_electronics():
    # 電装を追加するためのダイアログ
    electronics_type = simpledialog.askstring("電装の追加", "追加する電装の種類を入力してください：")
    if electronics_type:
        print(f"電装「{electronics_type}」を追加しました")


def add_missile():
    # ミサイルを追加するためのダイアログ
    missile_type = simpledialog.askstring("ミサイルの追加", "追加するミサイルの種類を入力してください：")
    if missile_type:
        print(f"ミサイル「{missile_type}」を追加しました")


def add_engine():
    # 機関を追加するためのダイアログ
    engine_type = simpledialog.askstring("機関の追加", "追加する機関の種類を入力してください：")
    if engine_type:
        print(f"機関「{engine_type}」を追加しました")


def remove_equipment():
    # 装備を削除するためのダイアログ
    equipment_type = simpledialog.askstring("装備の削除", "削除する装備の種類を入力してください：")
    if equipment_type:
        print(f"装備「{equipment_type}」を削除しました")




# ボタンを左右均等に配置
button_configs = [
    ("装甲追加ボタン", add_armor),
    ("砲塔追加ボタン", add_turret),
    ("魚雷追加ボタン", add_torpedo),
    ("対潜装備追加ボタン", add_asw),
    ("電装追加ボタン", add_electronics),
    ("ミサイル追加ボタン", add_missile),
    ("機関追加ボタン", add_engine),
    ("装備削除ボタン", remove_equipment),
]

for i, (text, command) in enumerate(button_configs):
    button = ttk.Button(left_frame, text=text, command=command)
    button.grid(row=len(labels) + i // 3, column=i % 3, padx=5, pady=5, sticky=tk.EW)

# 「shipファイルの出力ボタン」を左下に追加
def export():
    ship["開発年"] = entries["開発年"].get()
    ship["国家"] = entries["国家"].get()
    ship["艦型名"] = entries["艦型名"].get()
    ship["艦種"] = entries["級"].get()
    ship["全長"] = entries["全長"].get()
    ship["全幅"] = entries["全幅"].get()
    ship["最高速度"] = entries["最高速度"].get()
    ship["巡航速度"] = entries["巡航速度"].get()
    ship["航続距離"] = entries["航続距離"].get()
    ship["燃料量"] = entries["燃料量"].get()

    ship_data = export_ship_str_build(ship)
    export_ship_file(ship_data)


output_button = ttk.Button(left_frame, text="shipファイルの出力", command=export)
output_button.grid(row=len(labels) + len(button_configs) // 3 + 1, column=0, columnspan=4, padx=5, pady=10,
                   sticky=tk.EW)
# 右側に装備リストを配置
ttk.Label(right_frame, text="装備リスト").pack(anchor=tk.W)
equip_listbox = tk.Listbox(right_frame, height=25, width=30)
equip_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# ウィンドウサイズ変更時にリサイズ対応
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

if __name__ == "__main__":
    root.mainloop()
