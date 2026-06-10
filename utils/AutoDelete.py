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

from os import *
from datetime import datetime
import sys
import os
from send2trash import send2trash

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import load_config

CONFIG = load_config("dist", "config")
CONFIG_AUTO_DELETE = CONFIG["AutoDelete"]


def AutoDelete():
    def GetConfig() -> tuple[bool, bool, bool, str]:
        data = load_config("dist", "config")

        cfg = data.get("AutoDeleteConfig", {})

        by_create_date = cfg.get("Por Data de Criação", False)
        by_last_modified_date = cfg.get("Por Data de Modificação", False)
        days_to_auto_delete = cfg.get("Dias para Auto Deletar", "0")

        return by_create_date, by_last_modified_date, days_to_auto_delete

    def scan_files(
        PATH_FILES,
    ):  # Escaneia os arquivos da pasta e trás as datas de criação e modificação
        Dias_Config = int(GetConfig()[2])
        File_Name = str()
        CreateDate = datetime.now()
        ModifyDate = datetime.now()
        with scandir(PATH_FILES) as entries:
            for entry in entries:
                if entry.is_file():
                    File_Name = entry.name
                    CreateDate = datetime.fromtimestamp(entry.stat().st_birthtime)
                    ModifyDate = datetime.fromtimestamp(entry.stat().st_mtime)
                # Validação de exclusão
                if CONFIG_AUTO_DELETE == True:
                    if (datetime.now() - CreateDate).days > Dias_Config:
                        if GetConfig()[0] == True:
                            if CONFIG["Enviar Para Lixeira"] == True:
                                send2trash(entry.path)
                            elif CONFIG["Excluir permanentemente"] == True:
                                remove(entry.path)
                        else:
                            print(f"Configuração de data de criação desativada")
                    else:
                        print(
                            f"Nenhum arquivo está a mais de  {Dias_Config} dias para ser excluído\n Por data de criação"
                        )

                    if GetConfig()[1] == True:
                        if (datetime.now() - ModifyDate).days > Dias_Config:
                            if CONFIG["Enviar Para Lixeira"] == True:
                                send2trash(entry.path)
                            elif CONFIG["Excluir permanentemente"] == True:
                                remove(entry.path)
                            print(
                                f"Arquivo {File_Name} excluído por data de modificação"
                            )
                        else:
                            print(
                                f"Nenhum arquivo está a mais de  {Dias_Config} dias para ser excluído\n Por data de modificação"
                            )
                    else:
                        print("Configuração de data de modificação desativada")
                else:
                    print("Configuração de auto-delete desativada")

    Ignore_Config = [
        "Folder",
        "AutoDelete",
        "AutoDeleteConfig",
        "Startup",
        "timeverification",
        "Enviar Para Lixeira",
        "Excluir permanentemente",
    ]
    if CONFIG_AUTO_DELETE == True:
        for folder in CONFIG:
            if folder in Ignore_Config:
                continue
            else:
                for subfolder in CONFIG["Folder"]:
                    subfolder = subfolder.upper().replace(".", "")
                    Absolute_Path = CONFIG["Folder"] + "\\" + folder + "\\" + subfolder
                    if path.exists(Absolute_Path):
                        scan_files(Absolute_Path)
                        print(f"A pasta {Absolute_Path} foi Encontrada")
                    else:
                        print(f"Pasta {Absolute_Path} não encontrada ou não existe")
    else:
        print("Configuração de auto-delete desativada")


if __name__ == "__main__":
    AutoDelete()
