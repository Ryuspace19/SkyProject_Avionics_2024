import os
import tkinter as tk
from tkinter import filedialog

def process_file(file_path):
    # ファイルの内容を読み込む
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # ステップ1: 各行のカンマ区切りデータ数をカウントし、ヘッダーに追加
    processed_lines = []
    for line in lines:
        data_count = line.count(',') + 1
        new_line = f"Header_{data_count},{line.strip()}\n"
        processed_lines.append(new_line)

    # 新しいファイル名を作成（_A1.txt）
    directory, original_filename = os.path.split(file_path)
    new_filename = os.path.splitext(original_filename)[0] + "_A1.txt"
    new_file_path = os.path.join(directory, new_filename)

    # 新しいファイルに書き込む
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        new_file.writelines(processed_lines)

    print(f"新しいファイルが {new_file_path} に保存されました。")

    # ステップ2: 各行のデータ数を整える
    final_lines = []
    target_data_count = 34

    for line in processed_lines:
        # 行をカンマで分割し、最初の部分を確認
        data = line.strip().split(',')
        header_value = int(data[0].replace('Header_', ''))

        if header_value != target_data_count:
            # 数値が34でない場合、指定のフォーマットに変換
            new_line = "Header_err,app:,num,0,RS,,GPS,,,,,,,,,,BNO,,,,BME,,,,ALT,,AIR,,PIL,,,ACC,,,\n"
        else:
            # そのままの行を使用
            new_line = line

        final_lines.append(new_line)

    # 新しいファイル名を作成（_A2.txt）
    new_filename_final = os.path.splitext(original_filename)[0] + "_A2.txt"
    new_file_path_final = os.path.join(directory, new_filename_final)

    # 新しいファイルに書き込む
    with open(new_file_path_final, 'w', encoding='utf-8') as new_file:
        new_file.writelines(final_lines)

    print(f"整理されたデータが {new_file_path_final} に保存されました。")

# ファイル選択ダイアログを開く
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

if file_path:
    process_file(file_path)
else:
    print("ファイルが選択されませんでした。")
