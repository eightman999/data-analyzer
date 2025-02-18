from datetime import datetime
from tkinter import filedialog

import tkinter as tk

def export_ship_file(ship_str):
    # tkinterの初期化
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示

    # ファイルを保存するダイアログの表示
    file_path = filedialog.asksaveasfilename(
        defaultextension=".ship",  # デフォルトの拡張子
        filetypes=[("Ship files", "*.ship"), ("All files", "*.*")],  # ファイルタイプ
        title="保存先を選択してください"  # ダイアログ上のタイトル
    )

    if file_path:  # 選択された場合
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(ship_str)
        print(f"XML内容を'{file_path}'に保存しました。")
    else:  # キャンセルされた場合
        print("保存がキャンセルされました。")

def export_ship_str_build(ship):
    str = ""
    now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now_date)
    # Example ship data
    # ship = {
    #     "開発年": "",
    #     "国家": "",
    #     "艦型名": "",
    #     "艦種": "",
    #     "全長": "",
    #     "全幅": "",
    #     "最高速度": "",
    #     "巡航速度": "",
    #     "航続距離": "",
    #     "燃料量": "",
    #     "装甲": {ship["装甲"][armor_name] = {
    #                 "種類": armor_type,
    #                 "最大圧": max_armor_thickness,
    #                 "最小圧": min_armor_thickness,
    #                 "部位": armor_section,
    #                 "装甲値": armor_stat,
    #             }},
    #     "砲塔": {},
    #     "魚雷": {},
    #     "対潜装備": {},
    #     "電装": {},
    #     "ミサイル": {},
    #     "機関": {}
    # }

    #Example output file
    # [name].ship (実際はXML形式)
    #<ship>
        #<makedate>EXAMPLE MAKE DATE</makedate>
        #<lastupdate>EXAMPLE LAST UPDATE</lastupdate>
        #<status>
            #<name>EXAMPLE CLASS</name>
            #<year>EXAMPLE YEAR</year>
            #<country>EXAMPLE COUNTRY</country>
            #<type>EXAMPLE TYPE</type>
            #<length>EXAMPLE LENGTH</length>
            #<width>EXAMPLE WIDTH</width>
            #<max_speed>EXAMPLE MAX SPEED</max_speed>
            #<cruise_speed>EXAMPLE CRUISE SPEED</cruise_speed>
            #<naval_range>EXAMPLE NAVAL RANGE</naval_range>
            #<fuel_amount>EXAMPLE FUEL AMOUNT</fuel_amount>
        #</status>
        #<modules>
            #<armor>
                #<Armor_name>EXAMPLE ARMOR NAME</Armor_name>
                #<Armor_type>EXAMPLE ARMOR TYPE</Armor_type>
                #<max_armor>EXAMPLE MAX ARMOR</max_armor>
                #<min_armor>EXAMPLE MIN ARMOR</min_armor>
                #<armor_section>EXAMPLE ARMOR SECTION</armor_section>
                #<armor_stat>EXAMPLE ARMOR STAT</armor_stat>
            #</armor>
            #<armor>
                #<Armor_name>EXAMPLE ARMOR NAME_B</Armor_name>
                #...
            #</armor>
            #...
        #</modules>
    #</ship>
    str += "<ship>\n"
    str += "\t<make_date>" + now_date + "</make_date>\n"
    str += "\t<last_update>" + now_date + "</last_update>\n"
    str += "\t<status>\n"
    str += "\t\t<name>" + ship["艦型名"] + "</name>\n"
    str += "\t\t<year>" + ship["開発年"] + "</year>\n"
    str += "\t\t<country>" + ship["国家"] + "</country>\n"
    str += "\t\t<type>" + ship["艦種"] + "</type>\n"
    str += "\t\t<length>" + ship["全長"] + "</length>\n"
    str += "\t\t<width>" + ship["全幅"] + "</width>\n"
    str += "\t\t<max_speed>" + ship["最高速度"] + "</max_speed>\n"
    str += "\t\t<cruise_speed>" + ship["巡航速度"] + "</cruise_speed>\n"
    str += "\t\t<naval_range>" + ship["航続距離"] + "</naval_range>\n"
    str += "\t\t<fuel_amount>" + ship["燃料量"] + "</fuel_amount>\n"
    str += "\t</status>\n"
    str += "\t<modules>\n"
    for key in ship["装甲"]:
        str += "\t\t<armor>\n"
        for key2 in ship["装甲"][key]:
            str += "\t\t\t<" + key2 + ">" + ship["装甲"][key][key2] + "</" + key2 + ">\n"
        str += "\t\t</armor>\n"

    str += "\t\t<turret>\n"
    for key in ship["砲塔"]:
        str += "\t\t\t<" + key + ">" + ship["砲塔"][key] + "</" + key + ">\n"
    str += "\t\t</turret>\n"
    str += "\t\t<torpedo>\n"
    for key in ship["魚雷"]:
        str += "\t\t\t<" + key + ">" + ship["魚雷"][key] + "</" + key + ">\n"
    str += "\t\t</torpedo>\n"
    str += "\t\t<ASW>\n"
    for key in ship["対潜装備"]:
        str += "\t\t\t<" + key + ">" + ship["対潜装備"][key] + "</" + key + ">\n"
    str += "\t\t</ASW>\n"
    str += "\t\t<electric>\n"
    for key in ship["電装"]:
        str += "\t\t\t<" + key + ">" + ship["電装"][key] + "</" + key + ">\n"
    str += "\t\t</electric>\n"
    str += "\t\t<missile>\n"
    for key in ship["ミサイル"]:
        str += "\t\t\t<" + key + ">" + ship["ミサイル"][key] + "</" + key + ">\n"
    str += "\t\t</missile>\n"
    str += "\t\t<engine>\n"
    for key in ship["機関"]:
        str += "\t\t\t<" + key + ">" + ship["機関"][key] + "</" + key + ">\n"
    str += "\t\t</engine>\n"
    str += "\t</modules>\n"
    str += "</ship>\n"


    return str

def equip():
    res=""
    return res


def module_to_ID(module):

    pass