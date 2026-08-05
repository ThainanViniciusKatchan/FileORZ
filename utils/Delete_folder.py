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

exts = exts.Extensions()


def ORZ_folders():
    if not main_folder or not path.exists(main_folder):
        print(f"\nPasta principal {main_folder} não encontrada!")
    else:
        has_deleted = False
        if Delete_folder.Getativado == True:
            for root, dirs, files in walk(main_folder, topdown=False):
                for dir_name in dirs:
                    folder_path = path.join(root, dir_name)
                    for ext in exts.all_category:
                        if dir_name.lower() == ext.lower():
                            for sub_folder in listdir(folder_path):
                                if len(listdir(path.join(root, folder_path, sub_folder))) < 1:
                                    sub_folder_path = path.join(folder_path, sub_folder)
                                    print(sub_folder_path)
                                    send2trash(sub_folder_path)
                                if len(listdir(path.join(root, folder_path))) < 1:
                                    print(folder_path)
                                    send2trash(folder_path)


if __name__ == "__main__":
    ORZ_folders()
