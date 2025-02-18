from cx_Freeze import setup, Executable
import sys
import os
# サブプロセスで使用するPythonスクリプトのディレクトリを追加
os.environ['TCL_LIBRARY'] = r'C:\path\to\your\python\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\path\to\your\python\tcl\tk8.6'
# ビルドオプションを設定
build_exe_options = {
    "packages": ["os", "tkinter", "serial", "subprocess"],
    "include_files": [
        "main_display.py",
        "dataAnalist.py",
        # ここに他に必要なファイルを追加
    ]
}
setup(
    name="HPA_PilotApplication",
    version="1.0",
    description="HPA Pilot Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("StartScreen.py", base=None)],
)