from os import scandir
from os import *
import io
from datetime import datetime
from model import load_config, json_path
import json

CONFIG = load_config()

PATH_FILES = CONFIG['Folder']

CONFIG_AUTO_DELETE = CONFIG['AutoDelete']


def GetConfig() -> tuple[bool, bool, bool, str]:
    data = load_config()

    cfg = data.get('AutoDeleteConfig', {})

    by_create_date = cfg.get('Por Data de Criação', False)
    by_last_open_date = cfg.get('Por Data de Abertura', False)
    by_last_modified_date = cfg.get('Por Data de Modificação', False)
    days_to_auto_delete = cfg.get('Dias para Auto Deletar', "0")

    return by_create_date, by_last_open_date, by_last_modified_date, days_to_auto_delete

def scan_files(): # Escaneia os arquivos da pasta e trás as datas de criação, modificação e acesso
    with scandir(PATH_FILES) as entries:
        for entry in entries:
            if entry.is_file():
                global File_Name
                File_Name = entry.name
                CreateDate = datetime.fromtimestamp(entry.stat().st_birthtime)
                ModifyDate = datetime.fromtimestamp(entry.stat().st_mtime)
                AccessDate = datetime.fromtimestamp(entry.stat().st_atime)

                Dias_Config = int(GetConfig()[3])

            # Validação de exclusão
            if CONFIG_AUTO_DELETE == True:
                if (datetime.now() - CreateDate).days > Dias_Config: 
                    if GetConfig()[0] == True:
                        remove(entry.path)
                        print(f"Arquivo {File_Name} excluído por data de criação")
                    else:
                        print(f"Configuração de data de criação desativada")
                else:
                    print(f"Nenhum arquivo está a mais de  {Dias_Config} dias para ser excluído\n Por data de criação")

                if (datetime.now() - AccessDate).days > Dias_Config:
                    if GetConfig()[1] == True:
                        remove(entry.path)
                        print(f"Arquivo {File_Name} excluído por data de acesso")
                    else:
                        print(f"Nenhum arquivo está a mais de  {Dias_Config} dias para ser excluído\n Por data de acesso")
                else:
                    print(f"Configuração de data de acesso desativada")

                if GetConfig()[2] == True:
                    if (datetime.now() - ModifyDate).days > Dias_Config:
                        remove(entry.path)
                        print(f"Arquivo {File_Name} excluído por data de modificação")
                    else:
                        print(f"Nenhum arquivo está a mais de  {Dias_Config} dias para ser excluído\n Por data de modificação")
                else:
                    print("Configuração de data de modificação desativada")          
            else:
                print("Configuração de auto-delete desativada")        

                    
if __name__ == "__main__":
    scan_files()