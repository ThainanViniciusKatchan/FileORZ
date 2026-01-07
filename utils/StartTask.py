import subprocess
import os
import sys
from utils.model import load_config

def start_task():
    SCRIPT_DIR = os.path.join(os.getcwd(), "dist", "FileORZ.exe")
    INSTALL_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'FileORZ')
    config = load_config()
    Startup = config.get("Startup", False)
    print("Caminho do arquivo: ", SCRIPT_DIR, 
    "\nCaminho do instalador: ", INSTALL_DIR)
    if Startup == False:
        subprocess.Popen(f'{SCRIPT_DIR}', shell=True)
    else:
        subprocess.Popen(f'{os.path.join(INSTALL_DIR, "FileORZ.exe")}', shell=True)
        