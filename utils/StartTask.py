import os
import ctypes
import psutil
import customtkinter as ctk
from tkinter import messagebox
from utils.model import load_config

def check_if_running(TaskName):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == TaskName:
            return True
    return False

def start_task():
    config = load_config()
    Startup = config.get("Startup", False)

    STATUS = check_if_running("FileORZ.exe")

    if STATUS == False and Startup == False:
       SCRIPT_DIR = os.path.join(os.getcwd(), "dist", "FileORZ.exe")
    else:
        SCRIPT_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'FileORZ', 'FileORZ.exe')

    if STATUS == False:
        if os.path.exists(SCRIPT_DIR):
            ctypes.windll.shell32.ShellExecuteW(
                None,
                'open',
                SCRIPT_DIR,
            None,
            None,
            1
            )
            return True
    else:
        messagebox.showinfo("Erro", "FileORZ.exe ja esta em execução")
        return False
