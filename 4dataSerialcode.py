import serial
import tkinter as tk

def read_from_serial():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        data = line.split(',')  # カンマでデータを分割
        if len(data) == 4:  # データが4つであることを確認
            label1.config(text=data[0])
            label2.config(text=data[1])
            label3.config(text=data[2])
            label4.config(text=data[3])
    root.after(100, read_from_serial)

# シリアルポートの設定（Arduinoの接続ポートを確認してください）
ser = serial.Serial('COM5', 115200)

# Tkinter UIの設定
root = tk.Tk()
root.title("Arduino Data Display")
root.geometry("800x400")

# ラベルを4つ作成してデータを表示
#label1 = tk.Label(root, text="", font=("Helvetica", 60))
#label1.pack(expand=True)

#label2 = tk.Label(root, text="", font=("Helvetica", 60))
#label2.pack(expand=True)

#label3 = tk.Label(root, text="", font=("Helvetica", 60))
#label3.pack(expand=True)

#label4 = tk.Label(root, text="", font=("Helvetica", 60))
#label4.pack(expand=True)
# ラベルを4つ作成してデータを表示
label1 = tk.Label(root, text="", font=("Helvetica", 48))
label2 = tk.Label(root, text="", font=("Helvetica", 48))
label3 = tk.Label(root, text="", font=("Helvetica", 48))
label4 = tk.Label(root, text="", font=("Helvetica", 48))

# ラベルを2x2のグリッドに配置
label1.grid(row=0, column=0, sticky="nsew")
label2.grid(row=0, column=1, sticky="nsew")
label3.grid(row=1, column=0, sticky="nsew")
label4.grid(row=1, column=1, sticky="nsew")

# グリッドの行と列の重みを設定
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
# シリアルからの読み取りを開始
root.after(100, read_from_serial)

# Tkinterのメインループを開始
root.mainloop()