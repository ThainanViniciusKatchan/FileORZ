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
from ui.config import open_config_window


def config_btn(COLORS, actions_frame, root):
    btn_config = customtkinter.CTkButton(
        actions_frame,
        text="⚙️  Configurações",
        command=lambda: open_config_window(root),
        fg_color=COLORS["button_secondary"],
        hover_color=COLORS["button_secondary_hover"],
        border_width=0,
        corner_radius=10,
        font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
        width=160,
        height=48,
    )
    btn_config.pack(side="left")


from utils import folder


def start_btn(COLORS, actions_frame):
    from ui.index import main_container, root, feedback_label
    from utils.StartTask import start_organizer

    main_container = main_container
    root = root
    feedback_label = feedback_label

    # Botão para iniciar a organização
    btn_Start_Organizer = customtkinter.CTkButton(
        actions_frame,
        text="🚀  Iniciar Organização",
        command=lambda: start_organizer(
            main_container, root, folder.Folder().Getfolder, feedback_label
        ),
        fg_color=COLORS["accent_success"],
        hover_color=COLORS["accent_success_hover"],
        corner_radius=10,
        border_width=0,
        font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
        width=200,
        height=48,
    )
    btn_Start_Organizer.pack(side="right")
