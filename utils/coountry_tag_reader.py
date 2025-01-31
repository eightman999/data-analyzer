import csv
import re
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# ファイル選択ダイアログを表示
Tk().withdraw()  # Tkinterのメインウィンドウを非表示にする
input_file = askopenfilename(title="Select input file")

# 読み込んだファイルのディレクトリとファイル名を取得
input_dir = os.path.dirname(input_file)
input_filename = os.path.basename(input_file)
output_filename = os.path.splitext(input_filename)[0] + '.csv'
csv_file = os.path.join(input_dir, output_filename)

# ファイルから行を読み込む
with open(input_file, mode='r', encoding='utf-8') as file:
    lines = file.readlines()

# 結果を格納するリスト
results = []

# 各行に対して処理
for line in lines:
    # 大文字三文字の抽出
    match_upper = re.match(r'([A-Z]{3})', line)
    upper_three = match_upper.group(1) if match_upper else ""

    # countries/ の後ろのテキスト（.txtを除く）の抽出
    match_country = re.search(r'countries/([\w\s]+)\.txt', line)
    country = match_country.group(1) if match_country else ""

    # # の後のテキストの抽出
    match_description = re.search(r'#(.+)', line)
    description = match_description.group(1).strip() if match_description else ""

    # リストに結果を追加
    results.append([upper_three, country, description])

# CSVファイルに結果を書き込む
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['TAG', '地域', 'JP'])  # ヘッダー行
    writer.writerows(results)

print(f"CSV file created: {csv_file}")