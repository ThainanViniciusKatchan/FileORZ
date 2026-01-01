import os
import time
import json

import sys

# Caminho do arquivo de configuração baseado na localização do FileORZ.py
if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

# Carregar as extensões do arquivo config.json
def load_extensions():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Converter para o formato esperado
    extensions = {}
    for category, exts in data.items():
        if category != "Folder" and category != "timeverification" and category != "Startup":
            if type(exts) == str:
                extensions[category.capitalize()] = [exts]
            else:
                extensions[category.capitalize()] = [ext for ext, enabled in exts.items() if enabled]
    return extensions

# pasta de downloads e extenção de arquivo
def organize_files():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    path = data["Folder"]
    print(path)
    files = os.listdir(path)
    extensions_to_include = load_extensions()

    # verificar se o arquivo ja existe
    found_files = {}
    # Mover os arquivos para a pasta referente ao tipo de arquivo e a extenção
    for file in files:
        filename, file_extension = os.path.splitext(file)
        for folder, extensions in extensions_to_include.items():
            if file_extension.lower() in extensions:
                new_folder = os.path.join(path, folder, file_extension.upper()[1:])
                if not os.path.exists(new_folder):
                    os.makedirs(new_folder)

                # Mudar nome do arquivo para evitar erro
                destination_file = os.path.join(new_folder, file)
                counter = 1
                while os.path.exists(destination_file):
                    new_filename = f"{filename}_{counter}{file_extension}"
                    destination_file = os.path.join(new_folder, new_filename)
                    counter += 1

                    os.rename(os.path.join(path, file), destination_file)

                if filename in found_files:
                    os.remove(os.path.join(path, file))
                else:
                    found_files[filename] = True
                    os.rename(os.path.join(path, file), destination_file)
                    break
#verificar a pasta a com o tempo determiado pelo usuário
if __name__ == "__main__":
    while True:
        organize_files()
        
        # Ler o tempo de verificação a cada ciclo para permitir atualizações em tempo real
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            time_verification = int(data.get("timeverification", 30))
        except:
            time_verification = 30
            
        time.sleep(time_verification)
