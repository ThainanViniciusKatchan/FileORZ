import subprocess
import os
import sys
from utils.model import load_config

INSTALL_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'FileORZ')
def start_task():
    config = load_config()
    Startup = config.get("Startup", False)
    if Startup == False:
        subprocess.Popen([os.path.join(os.path.dirname(__file__), ".\\dist\\FileORZ.exe")])
    else:
        subprocess.Popen([os.path.join(INSTALL_DIR, "FileORZ.exe")])
    


        
        