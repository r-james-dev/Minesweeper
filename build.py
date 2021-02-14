from cx_Freeze import *

include_files = ["assets/", "LICENSE"]

setup(
    name="Minesweeper",
    version="1.0",
    author="James Ryan",
    executables=[Executable(
        "main.py", shortcut_name="Minesweeper", shortcut_dir="DesktopFolder",
        base="Win32GUI", icon="assets/bomb-128x128.ico"
    )],
    options={"build_exe": {"include_files": include_files}}
)
