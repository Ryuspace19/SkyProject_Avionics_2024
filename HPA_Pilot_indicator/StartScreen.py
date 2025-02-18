import tkinter as tk
import subprocess
import os
import sys

# 現在のスクリプトのディレクトリを取得
if getattr(sys, 'frozen', False):
    # PyInstallerでパッケージ化されたとき
    current_dir = sys._MEIPASS
else:
    # 通常のPythonスクリプトとして実行されるとき
    current_dir = os.path.dirname(os.path.abspath(__file__))

# Tkinterの設定
root = tk.Tk()
root.geometry("800x600")  # ウィンドウサイズを指定
root.title("HPA_PilotApplication")

# フレームの作成と配置
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill="both")

# スタート画面の作成
def show_start_screen():
    start_label = tk.Label(main_frame, text="HPA_PilotApplication", font=('Helvetica', 40))
    start_label.pack(pady=50, anchor='center')

    input_frame = tk.Frame(main_frame)
    input_frame.pack(pady=20)

    save_name_label = tk.Label(input_frame, text="保存名:", font=('Helvetica', 20))
    save_name_label.grid(row=0, column=0, padx=10, pady=10)

    save_name_entry = tk.Entry(input_frame, font=('Helvetica', 20), width=30)
    save_name_entry.grid(row=0, column=1, padx=10, pady=10)

    def start_application():
        filename = save_name_entry.get() if save_name_entry.get() else "data_log"
        subprocess.Popen(["python", os.path.join(current_dir, "main_display.py"), filename])  # main_display.pyを実行
        root.destroy()  # 現在のスタート画面を閉じる

    start_button = tk.Button(main_frame, text="Start", font=('Helvetica', 30), command=start_application)
    start_button.pack(pady=20, anchor='center')

    credit_label = tk.Label(main_frame, text="@SkyProject_2022~2024", font=('Helvetica', 15))
    credit_label.pack(side='bottom', pady=10)

    exit_button = tk.Button(main_frame, text="システム終了", font=('Helvetica', 15), command=root.quit)
    exit_button.pack(side='bottom', anchor='sw', padx=10, pady=10)

show_start_screen()
root.mainloop()
