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

from ast import arguments
import os
import json
import sys
import winreg
import shutil

if getattr(sys, "frozen", False):
    INSTALL_DIR = os.path.dirname(sys.executable)
else:
    INSTALL_DIR = os.path.dirname(os.path.abspath(__file__))

# Local installation path
INSTALL_DIR = os.path.join(os.getenv("LOCALAPPDATA"), "Programs", "FileORZ")
os.chdir(INSTALL_DIR)


def script_dir():  # find the path of the script
    if getattr(sys, "frozen", False):
        # Compiled
        BASE_DIR = os.path.dirname(sys.executable)
        print("BASE_DIR Comp: " + BASE_DIR)
    else:
        # Development
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("BASE_DIR Dev: " + BASE_DIR)
    return BASE_DIR


NoInstallDir = os.path.join(script_dir())  # Receives the path of the current script


def json_path(folder, file):
    """
    Precisa passar os parametrso folder e file:
    folder = pasta onde o json está
    file = nome do json, não precisa do .json
    """
    search_path = [script_dir(), os.path.join(script_dir(), folder)]

    for path in search_path:
        path = os.path.join(path, f"{file}.json")
        if os.path.exists(path):
            print(f"{file}.json encontrado em: " + path)
            return os.path.abspath(path)

    raise FileNotFoundError(
        f"o arquivo {file}.json não encontrado em nenhuma das pastas de busca."
        "Verifique se o arquivo está presente em uma das seguintes pastas:"
        f"\n{search_path}"
    )


def load_config(folder, file):
    """
    Precisa passar os parametrso folder e file:
    folder = pasta onde o json está
    file = nome do json, não precisa do .json
    """
    with open(json_path(folder, file), "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(folder, file, config):
    """
    Precisa passar os seguintes parametros na seguinte ordem:
    folder, file, config
    folder = pasta onde o json está
    file = nome do json, não precisa do .json
    config = Qual configuração será alterada
    """
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils import StartUp

    Start = StartUp.StartUpSys()
    with open(json_path(folder, file), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    local_config_path = os.path.join(INSTALL_DIR, folder, f"{file}.json")
    local_config_path_no_install = os.path.join(NoInstallDir, f"{folder}\\{file}.json")
    if os.path.exists(INSTALL_DIR) and Start.GetEnabled == True:
        try:
            with open(local_config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao sincronizar config: {e}")
    if os.path.exists(NoInstallDir):
        try:
            with open(local_config_path_no_install, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao sincronizar config: {e}")


# Controla se o script está sendo executado como .exe ou .py
def get_app_path():
    if getattr(sys, "frozen", False):
        return sys.executable
    else:
        return os.path.abspath(__file__)


# Cria a chave do script no registro do Windows
def is_startup_enabled():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ,
        )
        valor_atual, _ = winreg.QueryValueEx(key, "FileORZ")
        winreg.CloseKey(key)
        return "--tray" in valor_atual and "FL_ORZ.exe" in valor_atual
    except FileNotFoundError:
        return False


def toggle_startup(enable):
    """Habilita ou desabilita o programa de iniciar com o windows"""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "FileORZ"

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS
        )

        if enable:
            # Definir a origem da pasta dist
            if getattr(sys, "frozen", False):
                # Se for compilado, script_dir() retorna a pasta onde o executável está
                source_dir = script_dir()
                source_dist = os.path.join(source_dir)
            else:
                # Se for script (.py), a pasta dist estará no diretório base
                source_dist = os.path.join(script_dir())

            target_dist = os.path.join(INSTALL_DIR)
            target_exe = os.path.join(target_dist, "FL_ORZ.exe")

            if not os.path.exists(source_dist):
                print(f"Erro: Pasta dist não encontrada em {source_dist}")
                return

            # 3. Copia a pasta inteira
            if os.path.normpath(source_dist) != os.path.normpath(target_dist):
                if os.path.exists(target_dist):
                    shutil.rmtree(
                        target_dist
                    )  # Remove para substituir por versão atualizada
                shutil.copytree(source_dist, target_dist)

            # 4. Registra no Windows apontando para o executável dentro da nova pasta dist copiada
            registro_valor = f'"{target_exe}" --tray'
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, registro_valor)
            print(f"Instalado e registrado em: {registro_valor}")

        else:
            # Remove a chave do registro no Windows
            try:
                winreg.DeleteValue(key, app_name)
                print("Registro removido.")
            except FileNotFoundError:
                pass

                # Remove os arquivos e a pasta dist do AppData
            if os.path.exists(INSTALL_DIR):
                try:
                    shutil.rmtree(INSTALL_DIR)
                    print(f"Pasta removida: {INSTALL_DIR}")
                except Exception as e:
                    print(f"Erro ao remover pasta: {e}")

        winreg.CloseKey(key)
    except Exception as e:
        print(f"Erro ao alterar registro/arquivos: {e}")


if __name__ == "__main__":
    ...
