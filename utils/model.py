import os
import json
import sys
import winreg

# Caminho do arquivo de configuração
def script_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def json_path():
    return os.path.join(script_dir(), "config.json")

# Função para carregar a configuração
def load_config():
    with open(json_path(), 'r', encoding='utf-8') as f:
        return json.load(f)

# Função para salvar a configuração
def save_config(config):
    with open(json_path(), 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

# Carregar pasta atual salva
def get_current_folder():
    return load_config().get("Folder", "")

def set_current_folder(folder):
    config = load_config()
    config["Folder"] = folder
    save_config(config)

# Carrega o tempo de verificação
def get_time_verification():
    return load_config().get("timeverification", "5")

def set_time_verification(time):
    config = load_config()
    config["timeverification"] = time
    save_config(config)


# Função para habilitar a inicialização do script com o windows
def set_startup(var):
    config = load_config()
    config["Startup"] = var
    save_config(config)
    
def get_startup():
    return load_config().get("Startup", False)

# Controla o registro do windows para inicialização do script com o sistema
def get_app_path():
    """Retorna o caminho correto do executável ou do script python."""
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como .exe (PyInstaller)
        return sys.executable
    else:
        # Se estiver rodando como script .py
        return os.path.abspath(__file__)

def is_startup_enabled():
    """Verifica se o programa já está configurado para iniciar com o Windows."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, "FileORZ")
        winreg.CloseKey(key)
        return value == get_app_path()
    except FileNotFoundError:
        return False

def toggle_startup(enable):
    """Ativa ou desativa a inicialização automática."""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "FileORZ"
    app_path = get_app_path()

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        if enable:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, app_path)
            print(f"Registro adicionado: {app_path}")
        else:
            try:
                winreg.DeleteValue(key, app_name)
                print("Registro removido.")
            except FileNotFoundError:
                pass # Já não existia
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Erro ao alterar registro: {e}")