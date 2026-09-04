"""
Copyright (C) 2026 Thainan Vinicius Katchan

This file is part of FileORZ.

FileORZ is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FileORZ is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FileORZ.  If not, see <https://www.gnu.org/licenses/
"""

import os
import time
import json
import sys
from utils import AdvancedConfig
from utils import delete

# Adiciona o diretório raiz ao path para importações
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.model import json_path, load_config
from utils.translate import Translate
from utils.AutoDelete import AutoDelete
from utils.AdvancedConfig import AdvancedConfig
from utils.Delete_folder import ORZ_folders, all_folders
from utils.folder import Delete_Folde
from utils import exts
from AdvancedAlg import Alg

CONFIG_PATH = json_path("dist", "config")
WORKS_PATH = json_path("dist", "Key_Words")


# Carregar as extensões do arquivo category.json
def load_extensions():
    try:
        data = load_config("dist", "category")
        extensions = {}

        for category, exts in data.items():
            if isinstance(exts, dict):
                extensions[category] = [ext for ext, enabled in exts.items() if enabled]
            elif isinstance(exts, list):
                extensions[category] = exts
            elif isinstance(exts, str):
                extensions[category] = [exts]

        return extensions
    except Exception as e:
        print(f"Erro ao carregar extensões: {e}")
        return {}


# pasta para organizar e extenssão de arquivos
def organize_files():
    global data
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Erro ao carregar config: {e}")
        return

    # Definir o caminho original
    original_path = data.get("Folder", "")

    if not os.path.exists(original_path) or original_path == "":
        print(f"Diretório inválido ou não selecionado: {original_path}")
        return

    if not (os.access(original_path, os.R_OK) and os.access(original_path, os.W_OK)):
        print(f"Sem permissão de leitura/escrita em: {original_path}")
        return

    # Organize by extension and translate folders
    translator = Translate()
    extensions_to_include = load_extensions()
    extension_map = {}

    for category, exts in extensions_to_include.items():
        for ext in exts:
            clean_ext = ext.lower().strip()
            if not clean_ext.startswith("."):
                clean_ext = "." + clean_ext
            extension_map[clean_ext] = category

    try:
        with os.scandir(original_path) as entries:
            for entry in entries:
                if not entry.is_file() or entry.name.startswith("."):
                    continue

                filename, file_extension = os.path.splitext(entry.name)
                file_extension_lower = file_extension.lower()

                if file_extension_lower in extension_map:
                    raw_category = extension_map[file_extension_lower]
                    target_category = (
                        translator.get_text("category", raw_category)
                        or raw_category.capitalize()
                    )
                else:
                    target_category = (
                        translator.get_text("category", "other") or "OUTROS"
                    )

                sub_folder_name = (
                    file_extension.upper()[1:]
                    if len(file_extension) > 1
                    else (translator.get_text("category", "other") or "OUTROS")
                )
                new_folder = os.path.join(
                    original_path, target_category, sub_folder_name
                )
                os.makedirs(new_folder, exist_ok=True)

                destination_file = os.path.join(new_folder, entry.name)
                counter = 1
                while os.path.exists(destination_file):
                    new_filename = f"{filename}_{counter}{file_extension}"
                    destination_file = os.path.join(new_folder, new_filename)
                    counter += 1

                try:
                    print(f"Processando {entry.name}...", end=" ", flush=True)
                    os.rename(entry.path, destination_file)
                    print(f"[OK] -> {target_category}/{sub_folder_name}")
                except Exception as e:
                    print(f"[ERRO] {e}")
    except Exception as e:
        print(f"Erro ao ler diretório: {e}")


def loop_verification():
    print("Iniciando FileORZ Organizer...")
    while True:
        # AutoDelete empty folders
        del_folder = Delete_Folde()
        if del_folder.Getativado == True:
            if del_folder.Getpasta_orz == True:
                ORZ_folders()
            elif del_folder.Gettodas == True:
                all_folders()
        else:
            print("[INFO] Auto exclusão de pastas desabilitada.")

        # Advanced Organização
        if AdvancedConfig().get_enabled():
            Alg.processar_texto()
        else:
            print("[INFO] Organização avançada desabilitada.")

        # AutoDelete files
        autodelete = delete.AutoDelete().GetAutoDelete

        if autodelete == True:
            AutoDelete()
        else:
            print("[INFO] AutoDelete desabilitado.")
            pass

        # Files Organization
        if exts.Extensions().get_enable:
            organize_files()
        else:
            print("[INFO] ORZFiles desabilitado.")
            pass

        # Verification time
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            time_verification = float(data.get("timeverification", 5))
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            time_verification = 5

        print(f"\nAguardando {time_verification} minutos para a próxima verificação...")
        time.sleep(time_verification * 60)
