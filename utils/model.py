import os
import json
import sys
import winreg
import shutil

# Local installation path
INSTALL_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'FileORZ')

def script_dir(): # find the path of the script 
    if getattr(sys, 'frozen', False):
        # Compiled
        BASE_DIR = os.path.dirname(sys.executable)
        print("BASE_DIR Comp: " + BASE_DIR)
    else:
        # Development
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("BASE_DIR Dev: " + BASE_DIR)
    return BASE_DIR

NoInstallDir = os.path.join(script_dir()) # Receives the path of the current script 

def json_path(): # Performs a search to find the config.json file regardless of location
    search_path = [NoInstallDir, INSTALL_DIR, script_dir(), os.path.join(script_dir(), "dist")]

    for path in search_path:
        path = os.path.join(path, "config.json")
        if os.path.exists(path):
            print("config.json encontrado em: " + path)
            return os.path.abspath(path)

    raise FileNotFoundError(
        "config.json não encontrado em nenhuma das pastas de busca."
        "Verifique se o arquivo está presente em uma das seguintes pastas:"
        f"\n{search_path}"
    )

def load_config(): # Function that loads the settings
    with open(json_path(), 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config): # Function that saves the settings
    with open(json_path(), 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    # If installed in AppData, sync the config there too
    # so the background service receives the updates
    local_config_path = os.path.join(INSTALL_DIR, "config.json")
    local_config_path_no_install = os.path.join(NoInstallDir, "dist\\config.json")
    if os.path.exists(INSTALL_DIR) and get_startup() == True:
        try:
            with open(local_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao sincronizar config: {e}")
    if os.path.exists(NoInstallDir):
        try:
            with open(local_config_path_no_install, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao sincronizar config: {e}")

# Load saved current folder on config.json
def get_current_folder():
    return load_config().get("Folder", "")

def set_current_folder(folder):
    config = load_config()
    config["Folder"] = folder
    save_config(config)

# Load saved time verification on config.json
def get_time_verification():
    return load_config().get("timeverification", "5")

def set_time_verification(time):
    config = load_config()
    config["timeverification"] = time
    save_config(config)


# Function to enable the script to start with the windows
def set_startup(var):
    config = load_config()
    config["Startup"] = var
    save_config(config)
    
def get_startup():
    return load_config().get("Startup", False)

# Control the windows registry for the script to start with the system
def get_app_path():
    """Returns the correct path of the executable or the python script."""
    if getattr(sys, 'frozen', False):
        # If running as .exe (PyInstaller)
        return sys.executable
    else:
        # If running as .py script
        return os.path.abspath(__file__)

def is_startup_enabled():
    """Checks if the program is already configured to start with the Windows."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, "FileORZ")
        winreg.CloseKey(key)
        target_exe = os.path.join(INSTALL_DIR, ".\\dist\\FileORZ.exe")
        return os.path.normpath(value) == os.path.normpath(target_exe)
    except FileNotFoundError:
        return False

def toggle_startup(enable):
    """Enables or disables automatic startup, moving files to AppData."""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "FileORZ"
    
    # Destination paths
    target_exe = os.path.join(INSTALL_DIR, "FileORZ.exe")
    target_config = os.path.join(INSTALL_DIR, "config.json")

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        
        if enable:
            # 1. Create folder if it doesn't exist
            if not os.path.exists(INSTALL_DIR):
                os.makedirs(INSTALL_DIR)
            
            # 2. Copy Executable
            if getattr(sys, 'frozen', False):
                # If running from the executable
                source_exe = sys.executable
            else:
                # If running from the script, get from the dist folder
                source_exe = os.path.join(script_dir(), "dist", "FileORZ.exe")
                if not os.path.exists(source_exe):
                    print(f"Erro: Executável não encontrado em {source_exe}")
                    return

            # Only copy if we are not running from the destination itself
            if os.path.normpath(source_exe) != os.path.normpath(target_exe):
                shutil.copy2(source_exe, target_exe)
            
            # 3. Copy Config
            current_config = json_path()
            shutil.copy2(current_config, target_config)

            # 4. Register in Windows pointing to the file in AppData
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, target_exe)
            print(f"Instalado e registrado em: {target_exe}")
            
        else:
            # remove registry key on Windows
            try:
                winreg.DeleteValue(key, app_name)
                print("Registro removido.")
            except FileNotFoundError:
                pass 
            
            # Remove files and folder from AppData
            if os.path.exists(INSTALL_DIR):
                try:
                    shutil.rmtree(INSTALL_DIR)
                    print(f"Pasta removida: {INSTALL_DIR}")
                except Exception as e:
                    print(f"Erro ao remover pasta: {e}")

        winreg.CloseKey(key)
    except Exception as e:
        print(f"Erro ao alterar registro/arquivos: {e}")