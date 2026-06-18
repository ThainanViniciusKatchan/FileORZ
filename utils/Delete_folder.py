from os import path, listdir, rmdir
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import folder

main_folder = folder.Folder().Getfolder

def delete_folder():
    if not main_folder or not path.exists(main_folder):
        print(f"Pasta {main_folder} não encontrada!")
        return

    has_deleted = False
    try:
        for root, dirs, files in os.walk(main_folder, topdown=False):
            for d in dirs:
                dir_path = path.join(root, d)
                try:
                    # Verifica se a pasta está vazia
                    if listdir(dir_path) == []:
                        print(f"Pasta {dir_path} foi excluida!")
                        rmdir(dir_path)
                        has_deleted = True
                except Exception as Error:
                    print(f"Erro ao excluir a pasta {dir_path}: {Error}")
    except Exception as e:
        print(f"Erro ao acessar a pasta {main_folder}: {e}")
        return

    if not has_deleted:
        print("Sem pastas vazias para excluir")

if __name__ == "__main__":
    delete_folder()