import serial
import tkinter as tk


def read_from_serial():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        label.config(text=line)
    root.after(100, read_from_serial)


# シリアルポートの設定（Arduinoの接続ポートを確認してください）
ser = serial.Serial('COM8', 115200)

# Tkinter UIの設定
root = tk.Tk()
root.title("Arduino Data Display")

root.geometry("800x600")

label = tk.Label(root, text="", font=("Helvetica", 150))
label.pack(expand=True)

# シリアルからの読み取りを開始
root.after(100, read_from_serial)

def change_background(event):
        root.configure(bg='red')
root.bind('<Return>',change_background)

# Tkinterのメインループを開始
root.mainloop()
