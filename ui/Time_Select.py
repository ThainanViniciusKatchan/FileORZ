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
from utils import timeVerification
from utils.translate import Translate

Time = timeVerification

def time_select(main_container, COLORS):
    t = Translate()
    time_card = customtkinter.CTkFrame(
        main_container,
        fg_color=COLORS["bg_secondary"],
        corner_radius=12,
        border_width=1,
        border_color=COLORS["border"]
    )
    time_card.pack(fill="x", pady=(0, 15))

    time_inner = customtkinter.CTkFrame(time_card, fg_color="transparent")
    time_inner.pack(fill="x", padx=20, pady=15)

    # Header do card
    time_header = customtkinter.CTkFrame(time_inner, fg_color="transparent")
    time_header.pack(fill="x")

    time_icon = customtkinter.CTkLabel(
        time_header,
        text="⏱️",
        font=customtkinter.CTkFont(size=18)
    )
    time_icon.pack(side="left")

    time_title = customtkinter.CTkLabel(
        time_header,
        text=t.get_text("time_selection", "time_title") or "Intervalo de Verificação (Minutos)",
        font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
        text_color=COLORS["text_primary"]
    )
    time_title.pack(side="left", padx=(8, 0))

    # Configuração do tempo de verificação
    time_value = Time.TimeVerification.Gettime(None)
    if time_value != "1" or not time_value:
        DropDownTimeValue = customtkinter.StringVar(value=time_value)
    else:
        DropDownTimeValue = customtkinter.StringVar(value="1")

    Time.TimeVerification(time_value).time()

    # Dropdown do tempo
    DropDown_time = customtkinter.CTkOptionMenu(
        time_header,
        fg_color=COLORS["dropdown_bg"],
        button_color=COLORS["accent_primary"],
        button_hover_color=COLORS["accent_hover"],
        text_color=COLORS["text_primary"],
        height=32,
        width=100,
        font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
        dropdown_fg_color=COLORS["dropdown_bg"],
        dropdown_text_color=COLORS["text_primary"],
        dropdown_hover_color=COLORS["accent_hover"],
        variable=DropDownTimeValue,
        command=lambda x: timeVerification.TimeVerification(x).time(),
        values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        dynamic_resizing=False,
        corner_radius=8
    )
    DropDown_time.pack(side="right")

    # Descrição
    time_desc = customtkinter.CTkLabel(
        time_inner,
        text=t.get_text("time_selection", "time_subtitle") or "Tempo em minutos entre cada verificação automática de novos arquivos",
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color=COLORS["text_secondary"],
        anchor="w"
    )
    time_desc.pack(fill="x", pady=(10, 0))

    def update_time_select_texts():
        tr = Translate()
        time_title.configure(
            text=tr.get_text("time_selection", "time_title") or "Intervalo de Verificação (Minutos)"
        )
        time_desc.configure(
            text=tr.get_text("time_selection", "time_subtitle") or "Tempo em minutos entre cada verificação automática de novos arquivos"
        )

    Translate.register_listener(update_time_select_texts)