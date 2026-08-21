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

from os import path, listdir, rmdir, walk
import sys
from send2trash import send2trash

sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from utils import folder, exts

main_folder = folder.Folder().Getfolder

Delete_folder = folder.Delete_Folde()

exts_obj = exts.Extensions()


def ORZ_folders():
    current_main_folder = folder.Folder().Getfolder
    del_folder = folder.Delete_Folde()
    if not current_main_folder or not path.exists(current_main_folder):
        print(f"\nPasta principal {current_main_folder} não encontrada!")
        return

    if del_folder.Getativado:
        for root, dirs, files in walk(current_main_folder, topdown=False):
            for dir_name in dirs:
                folder_path = path.join(root, dir_name)
                for ext in exts_obj.all_category:
                    if dir_name.lower() == ext.lower():
                        if path.exists(folder_path) and path.isdir(folder_path):
                            for sub_folder in listdir(folder_path):
                                sub_folder_path = path.join(folder_path, sub_folder)
                                try:
                                    if path.isdir(sub_folder_path) and len(listdir(sub_folder_path)) < 1:
                                        print(f"[AutoDelete Pasta] {sub_folder_path}")
                                        if del_folder.Getlixeira:
                                            send2trash(sub_folder_path)
                                        elif del_folder.Getexcluir_permanentemente:
                                            rmdir(sub_folder_path)
                                except Exception as Error:
                                    print(Error)
                        try:
                            if path.exists(folder_path) and len(listdir(folder_path)) < 1:
                                print(f"[AutoDelete Pasta] {folder_path}")
                                if del_folder.Getlixeira:
                                    send2trash(folder_path)
                                elif del_folder.Getexcluir_permanentemente:
                                    rmdir(folder_path)
                        except Exception as Error:
                            print(Error)


def all_folders():
    current_main_folder = folder.Folder().Getfolder
    del_folder = folder.Delete_Folde()
    if not current_main_folder or not path.exists(current_main_folder):
        print(f"\nPasta principal {current_main_folder} não encontrada!")
        return

    if del_folder.Getativado:
        for root, dirs, files in walk(current_main_folder, topdown=False):
            for dir_name in dirs:
                folder_path = path.join(root, dir_name)
                try:
                    if path.exists(folder_path) and path.isdir(folder_path) and len(listdir(folder_path)) < 1:
                        print(f"[AutoDelete Pasta] {folder_path}")
                        if del_folder.Getlixeira:
                            send2trash(folder_path)
                        elif del_folder.Getexcluir_permanentemente:
                            rmdir(folder_path)
                except Exception as Error:
                    print(Error)


if __name__ == "__main__":
    all_folders()
