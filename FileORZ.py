import os
import time
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import json_path

CONFIG_PATH = json_path()

# Carregar as extensões do arquivo config.json
def load_extensions():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Converter para o formato esperado
    extensions = {}
    for category, exts in data.items():
        if category != "Folder" and category != "timeverification" and category != "Startup":
            if isinstance(exts, str):
                extensions[category.capitalize()] = [exts]
            else:
                extensions[category.capitalize()] = [ext for ext, enabled in exts.items() if enabled]
    return extensions

# pasta para organizar e extenssão de arquivos
def organize_files():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    path = data["Folder"]
    print("Folder of organization: " + path)
    if not os.path.exists(path): # Checar se a pasta existe
        print(f"this folder {path} does not exist.")
        return
    elif os.path.exists(path) and os.path.isdir(path): # Checar se a pasta existe e se é uma pasta
        if os.access(path, os.R_OK) and os.access(path, os.W_OK): # Checar se a pasta tem permissão de leitura e escrita
            print(f"this folder {path} has read and write permission.")
            files = os.listdir(path)
        else:
            print(f"this folder {path} has no read and write permission.")
            return
    extensions_to_include = load_extensions() # Carregar as extensões do arquivo config.json

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

                # Mudar nome do arquivo para evitar conflitos
                source_file = os.path.join(path, file)
                destination_file = os.path.join(new_folder, file)
                counter = 1
                
                # Encontrar um nome disponível
                try:
                    with open(destination_file, 'rb', encoding='utf-8') as f:
                        f.read()
                        if os.path.exists(destination_file):
                            while os.path.exists(destination_file):
                                new_filename = f"{filename}_{counter}{file_extension}"
                                destination_file = os.path.join(new_folder, new_filename)
                                counter += 1
                except Exception as e:
                    print(f"Erro ao encontrar um nome disponível: {e}")
                    continue

                # Mover o arquivo apenas uma vez com o nome correto
                if os.path.exists(source_file):
                    os.rename(source_file, destination_file)
                    break
#verificar a pasta a com o tempo determinado pelo usuário
if __name__ == "__main__":
    while True:
        organize_files()
        
        # Ler o tempo de verificação a cada ciclo para permitir atualizações em tempo real
        try:
            with open(CONFIG_PATH, 'rb', encoding='utf-8') as f:
                data = json.load(f)
            time_verification = int(data.get("timeverification", 1))
        except (FileNotFoundError, json.JSONDecodeError):
            time_verification = 1
        time.sleep(time_verification * 60)
