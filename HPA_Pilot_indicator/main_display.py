import tkinter as tk
import serial
import threading
import time
import os
from serial.tools import list_ports
from concurrent.futures import ThreadPoolExecutor
import sys
import subprocess

# グローバル変数
ser = None
logging_active = True  # SDカードへのログが有効かどうかを管理
executor = ThreadPoolExecutor(max_workers=3)  # 最大3つのスレッドを使用
buffer = []  # データをバッファリングするリスト
buffer_size = 20  # 2秒分のデータ（20個）をバッファリング

# コマンドライン引数で保存名を取得、引数がない場合はデフォルト名を使用
filename = (sys.argv[1] + ".txt") if len(sys.argv) > 1 else "default_data_log.txt"

# Tkinterの設定
root = tk.Tk()
root.geometry("1300x800")

# 画面を4分割するための線を引く関数
def draw_lines(canvas):
    width = 1300
    height = 800
    # 垂直線
    canvas.create_line(width / 2, 0, width / 2, height, fill="black")
    # 水平線
    canvas.create_line(0, height / 2, width, height / 2, fill="black")

# キャンバスを作成して線を描画
canvas = tk.Canvas(root, width=1300, height=800)
canvas.pack()
draw_lines(canvas)

# 左上、右上、右下のラベルを作成して配置
label_speed_text = tk.Label(root, text="速度:", font=('Helvetica', 40))
label_speed_text.place(x=50, y=150)

label_rpm_text = tk.Label(root, text="回転数:", font=('Helvetica', 40))
label_rpm_text.place(x=670, y=150)

label_altitude_text = tk.Label(root, text="高度:", font=('Helvetica', 40))
label_altitude_text.place(x=50, y=500)

# 数値部分のラベルを作成して配置
label_speed_value = tk.Label(root, text="0.0", font=('Helvetica', 140))
label_speed_value.place(x=195, y=100)

label_rpm_value = tk.Label(root, text="0", font=('Helvetica', 140))
label_rpm_value.place(x=865, y=100)

label_altitude_value = tk.Label(root, text="0", font=('Helvetica', 140))
label_altitude_value.place(x=195, y=450)

# 単位のラベルを作成して配置
label_speed_unit = tk.Label(root, text="m/s", font=('Helvetica', 40))
label_speed_unit.place(x=555, y=315)

label_rpm_unit = tk.Label(root, text="rpm", font=('Helvetica', 40))
label_rpm_unit.place(x=1170, y=315)

label_altitude_unit = tk.Label(root, text="cm", font=('Helvetica', 40))
label_altitude_unit.place(x=555, y=625)

# バーの設定
bar_height = 280  # バーの高さ
bar_width = 50  # バーの幅
bar_canvas = tk.Canvas(root, width=bar_width, height=bar_height, bg='white', highlightthickness=1, highlightbackground='black')
bar_canvas.place(x=5, y=400)  # ALTの左側にバーを配置

# 右下にSDカードの状況を表示するラベル
label_sd_status = tk.Label(root, text="SD: NO", font=('Helvetica', 30))
label_sd_status.place(x=680, y=420)

# 右下に接続ボタンと状態ラベルを追加
label_connection_status = tk.Label(root, text="No Connection", font=('Helvetica', 20))
label_connection_status.place(x=800, y=540)

# COMポート選択用のドロップダウンメニューとラベル
com_label = tk.Label(root, text="COMポート:", font=('Helvetica', 20))
com_label.place(x=680, y=480)

# 利用可能なCOMポートのリストを取得
available_ports = [port.device for port in list_ports.comports()]

# COMポート選択メニューの変数
selected_com_port = tk.StringVar()
selected_com_port.set(available_ports[0] if available_ports else "")

com_menu = tk.OptionMenu(root, selected_com_port, *available_ports)
com_menu.config(font=('Helvetica', 20))
com_menu.place(x=840, y=475)

def connect_com():
    global ser
    com_port = selected_com_port.get()  # ドロップダウンから選択されたCOMポートを取得
    try:
        ser = serial.Serial(com_port, 115200)
        label_connection_status.config(text="Connected")
        start_data_update_thread()  # 並列処理を開始
    except serial.SerialException as e:
        label_connection_status.config(text="No Connection")
        print(f"Failed to open serial port: {e}")

connect_button = tk.Button(root, text="接続", font=('Helvetica', 20), command=connect_com)
connect_button.place(x=680, y=530)

# SDカードの状態をチェックする関数
def check_sd_card():
    if os.path.exists('D:/'):
        label_sd_status.config(text="SD: OK")
    else:
        label_sd_status.config(text="SD: NO")

# 受信データをSDカードに保存する関数
def save_data_to_sd(data):
    global logging_active, buffer
    if logging_active:
        # 改行を追加してデータをバッファに追加
        buffer.append(data + '\n')
        if len(buffer) >= buffer_size:
            try:
                with open(f'D:/{filename}', 'a') as file:
                    file.writelines(buffer)
                buffer.clear()  # バッファをクリア
            except Exception as e:
                print(f"Error saving data to SD card: {e}")

# 高度バーの更新関数
def update_alt_bar(alt_value):
    # 高度の値をバーの高さに反映（0~100の範囲）
    alt_percentage = max(0.0, min(float(alt_value) / 100.0, 1.0))  # 0~1.0の範囲に収める
    fill_height = bar_height * alt_percentage
    bar_canvas.delete("all")

    # バーの色を決定（100未満：緑、100以上：赤）
    if float(alt_value) >= 100.0:
        color = "red"
    else:
        color = "green"

    # 黒枠を再描画
    bar_canvas.create_rectangle(0, 0, bar_width, bar_height, outline='black')
    # バーを描画
    bar_canvas.create_rectangle(0, bar_height - fill_height, bar_width, bar_height, fill=color)

# データの更新関数
def update_data():
    while ser is not None and ser.is_open:
        try:
            start_time = time.time()  # タイミング計測開始
            line = ser.readline().decode('utf-8').strip()
            check_sd_card()  # SDカードの状態を更新
            save_data_to_sd(line)  # データをバッファに保存
            data = line.split(',')

            speed_value = None
            rpm_value = None
            altitude_value = None

            # データの解析
            for i in range(len(data)):
                if data[i] == "AIR":  # 速度
                    speed_value = data[i + 1]
                elif data[i] == "RS":  # 回転数
                    rpm_value = data[i + 1]
                elif data[i] == "ALT":  # 高度
                    altitude_value = data[i + 1]

            # 数値のラベルを更新
            if speed_value is not None:
                label_speed_value.config(text=speed_value)
            if rpm_value is not None:
                label_rpm_value.config(text=rpm_value)
            if altitude_value is not None:
                label_altitude_value.config(text=altitude_value)
                update_alt_bar(altitude_value)  # 高度バーの更新

            end_time = time.time()  # タイミング計測終了
            print(f"データ処理とバッファリングにかかった時間: {end_time - start_time:.6f}秒")

            time.sleep(0.025)  # 40Hzで更新

        except Exception as e:
            print(f"Error: {e}")

def start_data_update_thread():
    executor.submit(update_data)  # 並列にデータ更新を開始

# エンターキーが押された回数を追跡
enter_press_count = 0

# エンターキーを押したときに呼ばれる関数
def on_enter(event):
    global enter_press_count
    global ser
    global logging_active
    enter_press_count += 1

    if enter_press_count == 1:
        # 1回目のエンターキー押下：画面を赤に切り替え
        hide_all_widgets()
        canvas.create_rectangle(0, 0, 1300, 800, fill='red')

    elif enter_press_count == 2:
        # 2回目のエンターキー押下：SDカードへのログを停止し、dataAnalist.pyを実行
        logging_active = False
        if ser is not None and ser.is_open:
            ser.close()
        ser = None
        reset_to_data_analist()  # dataAnalist.pyを実行

# 全てのウィジェットを隠す関数
def hide_all_widgets():
    label_speed_text.place_forget()
    label_rpm_text.place_forget()
    label_altitude_text.place_forget()
    label_speed_value.place_forget()
    label_rpm_value.place_forget()
    label_altitude_value.place_forget()
    label_speed_unit.place_forget()
    label_rpm_unit.place_forget()
    label_altitude_unit.place_forget()
    label_sd_status.place_forget()
    label_connection_status.place_forget()
    com_label.place_forget()
    com_menu.place_forget()
    connect_button.place_forget()
    canvas.delete("all")
    bar_canvas.place_forget()

# dataAnalist.pyを実行する関数
def reset_to_data_analist():
    root.destroy()  # 現在の画面を閉じる
    subprocess.Popen(["python", os.path.join(os.path.dirname(__file__), "dataAnalist.py")])  # dataAnalist.pyを実行

# エンターキーのイベントをバインド
root.bind('<Return>', on_enter)

# Tkinterのメインループを開始
root.mainloop()