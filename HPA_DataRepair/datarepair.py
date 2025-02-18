import os
import tkinter as tk
from tkinter import filedialog
import re

def is_valid_data(value):
    # 数値かどうか、または期待される形式かどうかを確認
    return re.match(r'^-?\d+(\.\d+)?$', value) is not None

def average(val1, val2):
    return (val1 + val2) / 2

def find_next_valid_data(lines, current_index, col_index):
    # 次の有効なデータを探す
    for i in range(current_index + 1, len(lines)):
        data = lines[i].strip().split(',')
        if col_index < len(data) and is_valid_data(data[col_index]):
            return float(data[col_index])
    return None  # 有効なデータが見つからない場合

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    expected_columns = 33  # データ列数、ヘッダー以外の列

    for i, line in enumerate(lines):
        data = line.strip().split(',')

        if len(data) - 1 < expected_columns:  # ヘッダーを除いたデータ列数の確認
            # 欠損データがある場合、前後の行を参照して線形補完
            for j in range(1, len(data)):  # ヘッダーはスキップ
                if not is_valid_data(data[j]):
                    # 前後のデータを参照
                    prev_value = float(lines[i-1].strip().split(',')[j]) if i > 0 and j < len(lines[i-1].strip().split(',')) and is_valid_data(lines[i-1].strip().split(',')[j]) else None
                    next_value = find_next_valid_data(lines, i, j)

                    if prev_value is not None and next_value is not None:
                        data[j] = str(average(prev_value, next_value))
                    elif prev_value is not None:
                        data[j] = str(prev_value)
                    elif next_value is not None:
                        data[j] = str(next_value)
                    else:
                        data[j] = '0'  # 補完できない場合は0にする

        new_line = ','.join(data) + '\n'
        new_lines.append(new_line)

    # 新しいファイル名を作成
    directory, original_filename = os.path.split(file_path)
    new_filename = os.path.splitext(original_filename)[0] + "_corrected.txt"
    new_file_path = os.path.join(directory, new_filename)

    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        new_file.writelines(new_lines)

    print(f"修正されたデータが {new_file_path} に保存されました。")

# ファイル選択ダイアログを開く
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

if file_path:
    process_file(file_path)
else:
    print("ファイルが選択されませんでした。")
