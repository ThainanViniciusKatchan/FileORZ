import os
import time
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import json_path

CONFIG_PATH = json_path()

# Carregar as extensões do arquivo config.json
def load_extensions():
    # Lê o config.json e retorna dicionário com tratamento de erros.
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        extensions = {}
        # Lista negra de chaves que não são categorias de arquivos
        ignored_keys = {"Folder", "timeverification", "Startup"}

        for category, exts in data.items():
            if category not in ignored_keys:
                # Normaliza o nome da categoria (ex: imAgens -> Imagens)
                cat_name = category.capitalize()
                
                if isinstance(exts, str):
                    extensions[cat_name] = [exts]
                elif isinstance(exts, dict):
                    # Garante que só processa se for dicionário mesmo
                    extensions[cat_name] = [ext for ext, enabled in exts.items() if enabled]
                    
        return extensions
    except Exception as e:
        print(f"Erro ao carregar extensões: {e}")
        return {}

# pasta para organizar e extenssão de arquivos
def organize_files():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Definir o caminho original
    original_path = data["Folder"] 
    print("Folder of organization: " + original_path)
    
    if not os.path.exists(original_path):
        print(f"this folder {original_path} does not exist.")
        return
    elif os.path.exists(original_path) and os.path.isdir(original_path):
        if not (os.access(original_path, os.R_OK) and os.access(original_path, os.W_OK)):
            print(f"this folder {original_path} has no read and write permission.")
            return
    extensions_to_include = load_extensions()
    extension_map = {}
    
    # variável 'path' sobrescrita: Usando 'category' em vez de 'path' no loop
    for category, exts in extensions_to_include.items():
        for ext in exts:
            clean_ext = ext.lower().strip()
            if not clean_ext.startswith('.'):
                clean_ext = '.' + clean_ext
            extension_map[clean_ext] = category
    try:
        # Usando a variável correta (original_path)
        with os.scandir(original_path) as entries:
            for entry in entries:
                # Se NÃO for arquivo (ou seja, for pasta) OU for oculto, PULA.
                if not entry.is_file() or entry.name.startswith("."):
                    continue
                filename, file_extension = os.path.splitext(entry.name)
                file_extension_lower = file_extension.lower()
                # lógica de categoria
                if file_extension_lower in extension_map:
                    target_category = extension_map[file_extension_lower]
                else:
                    target_category = "OUTROS"
                sub_folder_name = file_extension.upper()[1:] if len(file_extension) > 1 else "OUTROS"
                new_folder = os.path.join(original_path, target_category, sub_folder_name)
                os.makedirs(new_folder, exist_ok=True)
                destination_file = os.path.join(new_folder, entry.name)
                counter = 1
                while os.path.exists(destination_file):
                   new_filename = f"{filename}_{counter}{file_extension}" 
                   destination_file = os.path.join(new_folder, new_filename)
                   counter += 1
                
                try:
                    print(f"Processando {entry.path}...", end=" ", flush=True)
                    os.rename(entry.path, destination_file)
                    print(f"[OK] Movendo {entry.path} -> {destination_file}")
                except PermissionError:
                    print(f"[ERRO] Erro ao mover {entry.path}: Permissão negada.")
                except Exception as e:
                    print(f"[ERRO] Erro ao mover: {e}")
    except Exception as e:
        print(f"Erro ao ler diretório: {e}")
                    
#verificar a pasta a com o tempo determinado pelo usuário
if __name__ == "__main__":
    while True:
        organize_files()
        
        # Ler o tempo de verificação a cada ciclo para permitir atualizações em tempo real
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            time_verification = float(data.get("timeverification", 1))
        except (FileNotFoundError, json.JSONDecodeError):
            time_verification = 1
        time.sleep(time_verification * 60)
