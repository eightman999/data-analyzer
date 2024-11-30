import csv
import re
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

# ディレクトリ選択ダイアログを表示
Tk().withdraw()  # Tkinterのメインウィンドウを非表示にする
directory = askdirectory(title="Select directory")

# 出力ファイル名を設定
csv_file = os.path.join(directory, 'cap_list.csv')

# ファイル名パターンとcapitalパターンの定義
capital_pattern = re.compile(r'capital\s*=\s*(\d{1,5})')
land_tech_pattern = re.compile(r'land_tech_level_([a-zA-Z0-9])\s*=\s*yes')
support_tech_pattern = re.compile(r'support_tech_level_([a-zA-Z0-9])\s*=\s*yes')
tank_tech_pattern = re.compile(r'tank_tech_level_([a-zA-Z0-9])\s*=\s*yes')
air_tech_pattern = re.compile(r'air_tech_level_([a-zA-Z0-9])\s*=\s*yes')
navy_tech_pattern = re.compile(r'navy_tech_level_([a-zA-Z0-9])\s*=\s*yes')
indastry_tech_pattern = re.compile(r'industry_tech_level_([a-zA-Z0-9])\s*=\s*yes')
doctorine_tech_pattern = re.compile(r'doctrine_set_([a-zA-Z0-9])\s*=\s*yes')
political_set_id_pattern = re.compile(r'political_set_([a-zA-Z0-9])\s*=\s*yes')
set_tech_level_pattern = re.compile(r'set_tech_level_([a-zA-Z0-9])\s*=\s*yes')
popularities_set_pattern = re.compile(r'popularities_set_([a-zA-Z0-9])\s*=\s*yes')

# 結果を格納する辞書
capitals = {}
land_tech_levels = {}
support_tech_levels = {}
tank_tech_levels = {}
air_tech_levels = {}
navy_tech_levels = {}
indastry_tech_levels = {}
doctorine_set_ids = {}
political_set_ids = {}
tech_levels = {}
popularities_sets = {}

read_file = 0

# 指定したディレクトリからファイルを読み込む
for filename in os.listdir(directory):
    if filename == '.DS_Store':
        continue
    filepath = os.path.join(directory, filename)
    read_file += 1
    print(f"Reading {filepath}...")
    with open(filepath, mode='r', encoding='utf-8') as file:
        content = file.read()

        # Initialize variables with -1
        capital = '-'
        land_tech_level = '-'
        support_tech_level = '-'
        tank_tech_level = '-'
        air_tech_level = '-'
        navy_tech_level = '-'
        indastry_tech_level = '-'
        doctorine_set_id = '-'
        political_set_id = '-'
        tech_level = '-'
        popularities_set = '-'

        # Perform regex matching
        capital_match = capital_pattern.search(content)
        land_tech_match = land_tech_pattern.search(content)
        support_tech_match = support_tech_pattern.search(content)
        tank_tech_match = tank_tech_pattern.search(content)
        air_tech_match = air_tech_pattern.search(content)
        navy_tech_match = navy_tech_pattern.search(content)
        indastry_tech_match = indastry_tech_pattern.search(content)
        doctorine_tech_match = doctorine_tech_pattern.search(content)
        political_set_id_match = political_set_id_pattern.search(content)
        tech_level_match = set_tech_level_pattern.search(content)
        popularities_set_match = popularities_set_pattern.search(content)

        # Update variables if matches are found
        if capital_match:
            capital = capital_match.group(1)
        if land_tech_match:
            land_tech_level = land_tech_match.group(1)
        if support_tech_match:
            support_tech_level = support_tech_match.group(1)
        if tank_tech_match:
            tank_tech_level = tank_tech_match.group(1)
        if air_tech_match:
            air_tech_level = air_tech_match.group(1)
        if navy_tech_match:
            navy_tech_level = navy_tech_match.group(1)
        if indastry_tech_match:
            indastry_tech_level = indastry_tech_match.group(1)
        if doctorine_tech_match:
            doctorine_set_id = doctorine_tech_match.group(1)
        if political_set_id_match:
            political_set_id = political_set_id_match.group(1)
        if tech_level_match:
            tech_level = tech_level_match.group(1)
        if popularities_set_match:
            popularities_set = popularities_set_match.group(1)

        # Store results in dictionaries
        country_code = filename[:3]
        capitals[country_code] = capital
        land_tech_levels[country_code] = land_tech_level
        support_tech_levels[country_code] = support_tech_level
        tank_tech_levels[country_code] = tank_tech_level
        air_tech_levels[country_code] = air_tech_level
        navy_tech_levels[country_code] = navy_tech_level
        indastry_tech_levels[country_code] = indastry_tech_level
        doctorine_set_ids[country_code] = doctorine_set_id
        political_set_ids[country_code] = political_set_id
        tech_levels[country_code] = tech_level
        popularities_sets[country_code] = popularities_set

# countries_list.csvファイルを読み込み、capital列とLTL列を更新
countries_list_path = 'countries_list.csv'
updated_rows = []
print(f"Read {read_file} files.")
with open(countries_list_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        tag = row['TAG']
        if tag in capitals:
            row['capital'] = capitals[tag]
        if tag in land_tech_levels:
            row['LTL'] = land_tech_levels[tag]
        if tag in support_tech_levels:
            row['STL'] = support_tech_levels[tag]
        if tag in tank_tech_levels:
            row['TTL'] = tank_tech_levels[tag]
        if tag in air_tech_levels:
            row['ATL'] = air_tech_levels[tag]
        if tag in navy_tech_levels:
            row['NTL'] = navy_tech_levels[tag]
        if tag in indastry_tech_levels:
            row['ITL'] = indastry_tech_levels[tag]
        if tag in doctorine_set_ids:
            row['DID'] = doctorine_set_ids[tag]
        if tag in political_set_ids:
            row['PID'] = political_set_ids[tag]
        if tag in tech_levels:
            row['TL'] = tech_levels[tag]
        if tag in popularities_sets:
            row['PS'] = popularities_sets[tag]
        updated_rows.append(row)

# 更新された内容をcountries_list.csvに書き込む
with open(countries_list_path, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['TAG', '地域', 'JP', 'capital', 'LTL', 'STL', 'TTL', 'ATL', 'NTL','ITL','DID','PID','TL','PS']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"CSV file updated: {countries_list_path}")