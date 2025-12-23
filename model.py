import os
import json

# Caminho do arquivo de configuração
def script_dir():
    return os.path.dirname(os.path.abspath(__file__))
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

# Carrega o tempo de verificação
def get_time_verification():
    return load_config().get("timeverification", "5")    
