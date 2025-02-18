import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
import os
import subprocess

# グローバル変数としてファイルパスとグラフウィンドウ、地図ウィンドウを管理
file_path = None
root = None
graph_window = None
map_window = None
map_filename = None

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

def show_graph_window():
    try:
        global graph_window, map_filename
        graph_window = tk.Toplevel()
        graph_window.title("グラフ表示")
        graph_window.geometry("1920x1080")

        fig, axs = plt.subplots(2, 2, figsize=(18, 12))

        first_date, first_time, rs_data, bno_data, alt_data, air_data, gps_data = process_file(file_path)
        max_length = max(len(rs_data), len(bno_data['x']), len(alt_data), len(air_data))
        rs_index = np.arange(len(rs_data))
        bno_index = np.arange(len(bno_data['x']))
        alt_index = np.arange(len(alt_data))
        air_index = np.arange(len(air_data))

        axs[0, 0].plot(rs_index, rs_data, label='RS (rpm)', color='blue')
        axs[0, 0].set_title('RS (rpm)')
        axs[0, 0].set_xlabel('Index')
        axs[0, 0].set_ylabel('RS (rpm)')
        axs[0, 0].grid(True)
        axs[0, 0].set_xlim([0, max_length])

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

        if alt_data:
            axs[1, 0].plot(alt_index, alt_data, label='ALT (cm)', color='purple')
            axs[1, 0].set_title('ALT (cm)')
            axs[1, 0].set_xlabel('Index')
            axs[1, 0].set_ylabel('Altitude (cm)')
            axs[1, 0].grid(True)
            axs[1, 0].set_xlim([0, max_length])

        if air_data:
            axs[1, 1].plot(air_index, air_data, label='AIR (m/s)', color='brown')
            axs[1, 1].set_title('AIR (m/s)')
            axs[1, 1].set_xlabel('Index')
            axs[1, 1].set_ylabel('Speed (m/s)')
            axs[1, 1].grid(True)
            axs[1, 1].set_xlim([0, max_length])

        if first_date and first_time:
            plt.figtext(0.5, 0.98, f'Date: {first_date} Time: {first_time}', ha='center', fontsize=12)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        show_map_button = tk.Button(graph_window, text="地図表示", font=('Helvetica', 16, 'bold'), fg='red', command=show_map_window)
        show_map_button.pack(pady=20)
        show_map_button.place(relx=0.51, rely=0.5, anchor='center')

        if map_filename:
            file_label = tk.Label(graph_window, text=f"地図ファイル: {os.path.basename(map_filename)}", font=('Helvetica', 14))
            file_label.pack(pady=10)
            file_label.place(relx=0.55, rely=0.5, anchor='w')

        quit_button = tk.Button(graph_window, text="終了", font=('Helvetica', 16, 'bold'), fg='red', command=on_quit)
        quit_button.pack(pady=20)
        quit_button.place(relx=0.51, rely=0.97, anchor='center')
    except Exception as e:
        print(f"Error in show_graph_window: {e}")

def show_map_window():
    global map_filename
    try:
        if map_filename and os.path.exists(map_filename):
            webbrowser.open(f"file://{os.path.abspath(map_filename)}")
        else:
            messagebox.showerror("エラー", "地図ファイルが見つかりませんでした。")
    except Exception as e:
        print(f"Error in show_map_window: {e}")

def process_file(file_path, display_map=True):
    global map_filename
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        first_date = None
        first_time = None

        rs_data = []
        bno_data = {'x': [], 'y': [], 'z': []}
        alt_data = []
        air_data = []
        gps_data = []

        for i, line in enumerate(lines):
            if 'RS' in line and 'BNO' in line and 'ALT' in line and 'AIR' in line and 'GPS' in line:
                parts = line.split(',')
                try:
                    if i == 0:
                        first_date = parts[parts.index('GPS') + 1]
                        first_time = parts[parts.index('GPS') + 2]

                    rs_value = abs(float(parts[parts.index('RS') + 1]))
                    rs_data.append(rs_value)

                    bno_index = parts.index('BNO')
                    bno_data['x'].append(float(parts[bno_index + 1]))
                    bno_data['y'].append(float(parts[bno_index + 2]))
                    bno_data['z'].append(float(parts[bno_index + 3]))

                    alt_value = float(parts[parts.index('ALT') + 1])
                    alt_data.append(alt_value)

                    air_value = float(parts[parts.index('AIR') + 1])
                    air_data.append(air_value)

                    gps_index = parts.index('GPS')
                    lat = float(parts[gps_index + 3])
                    long = float(parts[gps_index + 4])
                    gps_data.append((lat, long))

                except (ValueError, IndexError) as e:
                    continue

        if display_map and gps_data:
            save_dir = "C:/Users/ryuai/OneDrive/プロジェクト/Sky Project/HPAC24フォルダ/電装/各システム/ソフトウェア/ソースコード/HPA_Pilot_indicator/maps"

            # ディレクトリが存在しない場合は作成する
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            map_filename = os.path.join(save_dir, 'map_with_gps.html')
            if os.path.exists(map_filename):
                base, ext = os.path.splitext(map_filename)
                counter = 1
                while os.path.exists(f"{base}_{counter}{ext}"):
                    counter += 1
                map_filename = f"{base}_{counter}{ext}"

            m = folium.Map(location=gps_data[0], zoom_start=15)
            marker_cluster = MarkerCluster().add_to(m)

            for lat, long in gps_data:
                folium.Marker(location=[lat, long]).add_to(marker_cluster)

            m.save(map_filename)
            print(f"GPSデータをプロットした地図を '{map_filename}' に保存しました。")
        else:
            map_filename = None  # 地図が生成されなかった場合にNoneを設定

        return first_date, first_time, rs_data, bno_data, alt_data, air_data, gps_data
    except Exception as e:
        print(f"Error in process_file: {e}")
        return None, None, [], {'x': [], 'y': [], 'z': []}, [], [], []

def on_quit():
    try:
        root.destroy()
        subprocess.Popen(["python", os.path.join(os.path.dirname(__file__), "StartScreen.py")])
    except Exception as e:
        print(f"Error in on_quit: {e}")

select_file()
root.mainloop()
