import tkinter as tk
import serial
import threading
import time
import os

# グローバル変数
ser = None
logging_active = True  # SDカードへのログが有効かどうかを管理

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
label_air = tk.Label(root, text="AIR: ", font=('Helvetica', 70))
label_air.place(x=150, y=150)

label_rs = tk.Label(root, text="RS: ", font=('Helvetica', 70))
label_rs.place(x=750, y=150)

label_alt = tk.Label(root, text="ALT: ", font=('Helvetica', 70))
label_alt.place(x=150, y=500)

# バーの設定
bar_height = 200  # バーの高さ
bar_width = 50  # バーの幅
bar_canvas = tk.Canvas(root, width=bar_width, height=bar_height, bg='white', highlightthickness=1, highlightbackground='black')
bar_canvas.place(x=80, y=450)  # ALTの左側にバーを配置

# 右下にSDカードの状況を表示するラベル
label_sd_status = tk.Label(root, text="SD: NO", font=('Helvetica', 30))
label_sd_status.place(x=680, y=420)

# 右下に接続ボタンと状態ラベルを追加
label_connection_status = tk.Label(root, text="No Connection", font=('Helvetica', 20))
label_connection_status.place(x=1050, y=650)

def connect_com():
    global ser
    try:
        ser = serial.Serial('COM15', 115200)
        label_connection_status.config(text="Connected")
        root.after(100, update_gui)  # 100msごとにデータ更新
    except serial.SerialException as e:
        label_connection_status.config(text="No Connection")
        print(f"Failed to open serial port: {e}")

connect_button = tk.Button(root, text="接続", font=('Helvetica', 20), command=connect_com)
connect_button.place(x=1050, y=600)

# SDカードの状態をチェックする関数
def check_sd_card():
    if os.path.exists('D:/'):
        label_sd_status.config(text="SD: OK")
    else:
        label_sd_status.config(text="SD: NO")

# 受信データをSDカードに保存する関数
def save_data_to_sd(data):
    global logging_active
    if logging_active:
        try:
            with open('D:/data_log.txt', 'a') as file:
                file.write(data + '\n')
        except Exception as e:
            print(f"Error saving data to SD card: {e}")

# ALTバーの更新関数
def update_alt_bar(alt_value):
    # ALTの値をバーの高さに反映（0~100の範囲）
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

# GUIの更新関数
def update_gui():
    if ser is not None and ser.is_open:
        try:
            line = ser.readline().decode('utf-8').strip()
            check_sd_card()  # SDカードの状態を更新
            save_data_to_sd(line)  # データをSDカードに保存
            data = line.split(',')

            air_value = None
            rs_value = None
            alt_value = None

            # データの解析
            for i in range(len(data)):
                if data[i] == "AIR":
                    air_value = data[i + 1]
                elif data[i] == "RS":
                    rs_value = data[i + 1]
                elif data[i] == "ALT":
                    alt_value = data[i + 1]

            # ラベルの更新
            if air_value is not None:
                label_air.config(text=f"AIR: {air_value}")
            if rs_value is not None:
                label_rs.config(text=f"RS: {rs_value}")
            if alt_value is not None:
                label_alt.config(text=f"ALT: {alt_value}")
                update_alt_bar(alt_value)  # ALTバーの更新

        except Exception as e:
            print(f"Error: {e}")

    root.after(100, update_gui)  # 100msごとにGUIを更新

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
        # 2回目のエンターキー押下：SDカードへのログを停止し、プログラムを待機状態にする
        logging_active = False
        if ser is not None and ser.is_open:
            ser.close()
        ser = None
        reset_background()  # 初期状態に戻す

# 全てのウィジェットを隠す関数
def hide_all_widgets():
    label_air.place_forget()
    label_rs.place_forget()
    label_alt.place_forget()
    label_sd_status.place_forget()
    label_connection_status.place_forget()
    connect_button.place_forget()
    canvas.delete("all")
    bar_canvas.place_forget()

# 背景を元に戻す関数
def reset_background():
    global enter_press_count
    canvas.delete("all")
    draw_lines(canvas)
    label_air.place(x=150, y=150)
    label_rs.place(x=750, y=150)
    label_alt.place(x=400, y=500)
    label_sd_status.place(x=1050, y=500)
    label_connection_status.place(x=1050, y=650)
    connect_button.place(x=1050, y=600)
    bar_canvas.place(x=300, y=500)
    root.configure(bg='SystemButtonFace')
    enter_press_count = 0  # エンターキー押下回数をリセット

# エンターキーのイベントをバインド
root.bind('<Return>', on_enter)

# Tkinterのメインループを開始
root.mainloop()
