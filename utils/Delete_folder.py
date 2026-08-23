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


def get_all_category_names():
    names = set(cat.lower() for cat in exts_obj.all_category)
    names.add("outros")
    names.add("other")
    try:
        from utils.model import script_dir, load_config
        locate_dir = path.join(script_dir(), "locate")
        if path.exists(locate_dir):
            for file in listdir(locate_dir):
                if file.endswith(".json"):
                    lang_code = path.splitext(file)[0]
                    try:
                        data = load_config("locate", lang_code)
                        cats = data.get("category", {})
                        for val in cats.values():
                            if isinstance(val, str):
                                names.add(val.lower())
                    except Exception:
                        pass
    except Exception:
        pass
    return names


def ORZ_folders():
    current_main_folder = folder.Folder().Getfolder
    del_folder = folder.Delete_Folde()
    if not current_main_folder or not path.exists(current_main_folder):
        print(f"\nPasta principal {current_main_folder} não encontrada!")
        return

    all_cat_names = get_all_category_names()

    if del_folder.Getativado:
        for root, dirs, files in walk(current_main_folder, topdown=False):
            for dir_name in dirs:
                folder_path = path.join(root, dir_name)
                if dir_name.lower() in all_cat_names:
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
