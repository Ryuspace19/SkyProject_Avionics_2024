import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
import os

# グローバル変数としてファイルパスとグラフウィンドウ、地図ウィンドウを管理
file_path = None
root = None
graph_window = None
map_window = None

# ファイル選択のUIを作成
def select_file():
    global file_path, root
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを隠す
    file_path = filedialog.askopenfilename(
        title="データファイルを選択してください",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if file_path:
        root.deiconify()  # メインウィンドウを再表示
        show_graph_window()  # グラフ画面を表示
    else:
        print("ファイルが選択されませんでした。")

# グラフ画面を表示
def show_graph_window():
    global graph_window
    graph_window = tk.Toplevel()
    graph_window.title("グラフ表示")
    graph_window.geometry("1920x1080")  # ウィンドウのサイズを指定

    # グラフを描画する
    fig, axs = plt.subplots(2, 2, figsize=(18, 12))

    # データを処理してグラフにプロット
    first_date, first_time, rs_data, bno_data, alt_data, air_data, gps_data = process_file(file_path)
    max_length = max(len(rs_data), len(bno_data['x']), len(alt_data), len(air_data))
    rs_index = np.arange(len(rs_data))
    bno_index = np.arange(len(bno_data['x']))
    alt_index = np.arange(len(alt_data))
    air_index = np.arange(len(air_data))

    # RSのグラフ (第一象限)
    axs[0, 0].plot(rs_index, rs_data, label='RS (rpm)', color='blue')
    axs[0, 0].set_title('RS (rpm)')
    axs[0, 0].set_xlabel('Index')
    axs[0, 0].set_ylabel('RS (rpm)')
    axs[0, 0].grid(True)
    axs[0, 0].set_xlim([0, max_length])

    # BNOのグラフ (第二象限)
    if bno_data['x'] and bno_data['y'] and bno_data['z']:
        axs[0, 1].plot(bno_index, bno_data['x'], label='BNO X', color='red')
        axs[0, 1].plot(bno_index, bno_data['y'], label='BNO Y', color='green')
        axs[0, 1].plot(bno_index, bno_data['z'], label='BNO Z', color='orange')
        axs[0, 1].set_title('BNO (Euler Angles)')
        axs[0, 1].set_xlabel('Index')
        axs[0, 1].set_ylabel('Angle (degrees)')
        axs[0, 1].legend()
        axs[0, 1].grid(True)
        axs[0, 1].set_xlim([0, max_length])

    # ALTのグラフ (第三象限)
    if alt_data:
        axs[1, 0].plot(alt_index, alt_data, label='ALT (cm)', color='purple')
        axs[1, 0].set_title('ALT (cm)')
        axs[1, 0].set_xlabel('Index')
        axs[1, 0].set_ylabel('Altitude (cm)')
        axs[1, 0].grid(True)
        axs[1, 0].set_xlim([0, max_length])

    # AIRのグラフ (第四象限)
    if air_data:
        axs[1, 1].plot(air_index, air_data, label='AIR (m/s)', color='brown')
        axs[1, 1].set_title('AIR (m/s)')
        axs[1, 1].set_xlabel('Index')
        axs[1, 1].set_ylabel('Speed (m/s)')
        axs[1, 1].grid(True)
        axs[1, 1].set_xlim([0, max_length])

    # 最初の日時データを表示
    if first_date and first_time:
        plt.figtext(0.5, 0.98, f'Date: {first_date} Time: {first_time}', ha='center', fontsize=12)

    # グラフの間のスペースを調整
    plt.tight_layout()

    # グラフを描画
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # 地図表示ボタンを中央に配置
    show_map_button = ttk.Button(graph_window, text="地図表示", command=show_map_window)
    show_map_button.pack(pady=20)
    show_map_button.place(relx=0.51, rely=0.5, anchor='center')

    # プログラム終了ボタンを中央に配置
    quit_button = ttk.Button(graph_window, text="終了", command=root.quit)
    quit_button.pack(pady=20)
    quit_button.place(relx=0.51, rely=0.97, anchor='center')

# 地図画面を表示
def show_map_window():
    global map_window
    map_window = tk.Toplevel()
    map_window.title("地図表示")
    map_window.geometry("1000x800")  # ウィンドウのサイズを指定

    # 地図を表示する
    process_file(file_path, display_map=True)

    # 地図を表示するために、保存されたHTMLファイルをWebブラウザで開く
    webbrowser.open('map_with_gps.html')

    # グラフ表示ボタンを中央に配置
    show_graph_button = ttk.Button(map_window, text="グラフ表示", command=show_graph_window)
    show_graph_button.pack(pady=20)
    show_graph_button.place(relx=0.5, rely=0.9, anchor='center')

# ファイルを処理してグラフと地図を表示
def process_file(file_path, display_map=False):
    # データを読み込んでリストに変換
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 最初の行から日時データを抽出
    first_date = None
    first_time = None

    # 抽出するデータのリスト
    rs_data = []
    bno_data = {'x': [], 'y': [], 'z': []}
    alt_data = []
    air_data = []
    gps_data = []  # GPSデータを保存するリスト

    # データを解析して各リストに追加
    for i, line in enumerate(lines):
        if 'RS' in line and 'BNO' in line and 'ALT' in line and 'AIR' in line and 'GPS' in line:
            parts = line.split(',')
            try:
                # 最初の行の日時データを取得
                if i == 0:
                    first_date = parts[parts.index('GPS') + 1]
                    first_time = parts[parts.index('GPS') + 2]

                # RSの値を抽出して絶対値に変換
                rs_value = abs(float(parts[parts.index('RS') + 1]))
                rs_data.append(rs_value)

                # BNOの値を抽出
                bno_index = parts.index('BNO')
                bno_data['x'].append(float(parts[bno_index + 1]))
                bno_data['y'].append(float(parts[bno_index + 2]))
                bno_data['z'].append(float(parts[bno_index + 3]))

                # ALTの値を抽出
                alt_value = float(parts[parts.index('ALT') + 1])
                alt_data.append(alt_value)

                # AIRの値を抽出
                air_value = float(parts[parts.index('AIR') + 1])
                air_data.append(air_value)

                # GPSの値を抽出
                gps_index = parts.index('GPS')
                lat = float(parts[gps_index + 3])  # 緯度
                long = float(parts[gps_index + 4])  # 経度
                gps_data.append((lat, long))

            except (ValueError, IndexError) as e:
                # データが不完全な場合はスキップ
                continue

    # 地図の作成と保存
    if display_map and gps_data:
        # 中心を最初のGPSデータに設定
        m = folium.Map(location=gps_data[0], zoom_start=15)

        # マーカーをクラスター化
        marker_cluster = MarkerCluster().add_to(m)

        # 各GPSポイントにマーカーを追加
        for lat, long in gps_data:
            folium.Marker(location=[lat, long]).add_to(marker_cluster)

        # 同じ名前のファイルが存在する場合、新しい名前で保存
        map_filename = 'map_with_gps.html'
        if os.path.exists(map_filename):
            base, ext = os.path.splitext(map_filename)
            counter = 1
            while os.path.exists(f"{base}_{counter}{ext}"):
                counter += 1
            map_filename = f"{base}_{counter}{ext}"

        # 地図を保存
        m.save(map_filename)
        print(f"GPSデータをプロットした地図を '{map_filename}' に保存しました。")

    return first_date, first_time, rs_data, bno_data, alt_data, air_data, gps_data

# ファイル選択UIを表示
select_file()

# tkinter のメインループを開始
root.mainloop()
