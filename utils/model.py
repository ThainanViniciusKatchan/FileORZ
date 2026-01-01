import os
import json
import sys
import winreg

import shutil

# Caminho de instalação local
INSTALL_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'FileORZ')

# Detecta o diretório base (diferente quando empacotado vs desenvolvimento)
def script_dir():
    if getattr(sys, 'frozen', False):
        # Empacotado pelo PyInstaller - usar diretório do executável
        return os.path.dirname(sys.executable)
    else:
        # Desenvolvimento - usar diretório do script
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NoInstallDir = os.path.join(script_dir(), "dist")

def json_path():
    if getattr(sys, 'frozen', False):
        # Quando empacotado, config.json está no mesmo diretório do executável
        return os.path.join(script_dir(), "config.json")
    else:
        # Em desenvolvimento
        return os.path.join(script_dir(), "dist", "config.json")

# Função para carregar a configuração
def load_config():
    with open(json_path(), 'r', encoding='utf-8') as f:
        return json.load(f)

# Função para salvar a configuração
def save_config(config):
    # Salva no local original (onde a UI está)
    with open(json_path(), 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    # Se estiver instalado no AppData, sincroniza a config lá também
    # para que o serviço em background receba as atualizações
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
        target_exe = os.path.join(INSTALL_DIR, ".\\dist\\FileORZ.exe")
        return os.path.normpath(value) == os.path.normpath(target_exe)
    except FileNotFoundError:
        return False

def toggle_startup(enable):
    """Ativa ou desativa a inicialização automática, movendo arquivos para AppData."""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "FileORZ"
    
    # Caminhos de destino
    target_exe = os.path.join(INSTALL_DIR, "FileORZ.exe")
    target_config = os.path.join(INSTALL_DIR, "config.json")

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        
        if enable:
            # 1. Criar pasta se não existir
            if not os.path.exists(INSTALL_DIR):
                os.makedirs(INSTALL_DIR)
            
            # 2. Copiar Executável
            if getattr(sys, 'frozen', False):
                # Se rodando do executável
                source_exe = sys.executable
            else:
                # Se rodando do script, pegar da pasta dist
                source_exe = os.path.join(script_dir(), "dist", "FileORZ.exe")
                if not os.path.exists(source_exe):
                    print(f"Erro: Executável não encontrado em {source_exe}")
                    return

            # Só copiamos se não estivermos rodando do próprio destino
            if os.path.normpath(source_exe) != os.path.normpath(target_exe):
                shutil.copy2(source_exe, target_exe)
            
            # 3. Copiar Config
            current_config = json_path()
            shutil.copy2(current_config, target_config)

            # 4. Registrar no Windows apontando para o arquivo no AppData
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, target_exe)
            print(f"Instalado e registrado em: {target_exe}")
            
        else:
            # Remover do registro
            try:
                winreg.DeleteValue(key, app_name)
                print("Registro removido.")
            except FileNotFoundError:
                pass 
            
            # Remover arquivos e pasta do AppData
            if os.path.exists(INSTALL_DIR):
                try:
                    shutil.rmtree(INSTALL_DIR)
                    print(f"Pasta removida: {INSTALL_DIR}")
                except Exception as e:
                    print(f"Erro ao remover pasta: {e}")

        winreg.CloseKey(key)
    except Exception as e:
        print(f"Erro ao alterar registro/arquivos: {e}")