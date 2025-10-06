import os
import platform
import subprocess
from tkinter.filedialog import askopenfilename, askopenfilenames
import eel

def get_file_path_by_name(file_name):
    for f in selected_files_list:
        if file_name in f:
            return f

def is_file_exec(file): return os.access(file, os.X_OK)

@eel.expose
def select_files():
    files_paths = askopenfilenames(title="Select python files", filetypes=[('Python Files', '*.py')])
    if files_paths is not None:
        if files_paths:
            if "selected_files_list" not in globals():
                global selected_files_list
                selected_files_list = set()
            selected_files_list = selected_files_list | set(files_paths)
            return list(files_paths)

@eel.expose
def select_interpreter():
    global py_interp
    if platform.system() == "Windows":
        py_interp = askopenfilename(title="Select python interpreter", filetypes=[('Python Interpreter', '*.exe')])
        return py_interp
    elif platform.system() == "Linux":
        py_interp = askopenfilename(title="Select python interpreter", filetypes=[('Python Interpreter', '*.*')])
        return py_interp if is_file_exec(py_interp) else ""

@eel.expose
def run_file(file):
    file_path = get_file_path_by_name(file)
    file_folder = get_file_path_by_name(file).split(file)[0]

    print(file_folder)
    
    if platform.system() == "Windows":
        subprocess.run(
            f'start cmd.exe @cmd /k "cd {file_folder} && {py_interp} {file_path}"',
            shell=True,
            check=True,
        )
    elif platform.system() == "Linux":
        subprocess.run(
            f'xfce4-terminal -e "cd {file_folder} && {py_interp} {file_path}"',
            shell=True,
            check=True,
        )