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

import customtkinter
from customtkinter import filedialog
from utils import folder
import os

Folder = folder.Folder


def folder_select(
    main_container,
    COLORS,
):
    folder_card = customtkinter.CTkFrame(
        main_container,
        fg_color=COLORS["bg_secondary"],
        corner_radius=12,
        border_width=1,
        border_color=COLORS["border"],
    )
    folder_card.pack(fill="x", pady=(0, 15))

    folder_inner = customtkinter.CTkFrame(folder_card, fg_color="transparent")
    folder_inner.pack(fill="x", padx=20, pady=15)

    # Ícone e título
    folder_header = customtkinter.CTkFrame(folder_inner, fg_color="transparent")
    folder_header.pack(fill="x")

    folder_icon = customtkinter.CTkLabel(
        folder_header, text="📂", font=customtkinter.CTkFont(size=18)
    )
    folder_icon.pack(side="left")

    folder_title = customtkinter.CTkLabel(
        folder_header,
        text="Selecionar Pasta para Organizar",
        font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
        text_color=COLORS["text_primary"],
    )
    folder_title.pack(side="left", padx=(8, 0))

    # Botão selecionar pasta
    def select_path():
        """Abre diálogo para selecionar pasta a ser organizada"""
        current_folder = Folder().Getfolder
        initial_dir = current_folder if os.path.exists(current_folder) else os.getcwd()

        selected_folder = filedialog.askdirectory(
            title="Selecione a pasta", initialdir=initial_dir
        )

        if selected_folder:
            Folder().folder = selected_folder
            # Atualiza o label com o caminho
            folder_path_label.configure(text=selected_folder)
            print(f"Pasta salva com sucesso: {selected_folder}")
        else:
            print("Nenhuma pasta selecionada")

    btn_Select_folder = customtkinter.CTkButton(
        folder_header,
        text="Selecionar",
        command=select_path,
        fg_color=COLORS["button_secondary"],
        hover_color=COLORS["button_secondary_hover"],
        border_width=0,
        corner_radius=8,
        font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
        width=120,
        height=32,
    )
    btn_Select_folder.pack(side="right")

    # Label mostrando caminho atual
    current_folder = Folder().Getfolder
    folder_path_label = customtkinter.CTkLabel(
        folder_inner,
        text=current_folder if current_folder else "Nenhuma pasta selecionada",
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color=COLORS["text_secondary"],
        anchor="w",
    )
    folder_path_label.pack(fill="x", pady=(10, 0))
