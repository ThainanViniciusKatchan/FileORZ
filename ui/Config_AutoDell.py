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
import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui.Centralizar_Janela import Centralizar_Janela
from utils import delete, timeVerification
from utils.model import load_config, save_config

row = 0
col = 6

config = load_config("dist", "config")

COLORS = {
    "bg_primary": "#0D0D0D",
    "bg_secondary": "#1A1A2E",
    "bg_card": "#16213E",
    "bg_card_inner": "#121228",
    "accent_primary": "#9D4EDD",
    "accent_hover": "#7B2CBF",
    "accent_success": "#06D6A0",
    "accent_success_hover": "#05B88A",
    "accent_danger": "#EF476F",
    "accent_danger_hover": "#D63D5E",
    "text_primary": "#FFFFFF",
    "text_secondary": "#A0A0A0",
    "text_category": "#9D4EDD",
    "border": "#2D2D44",
    "checkbox_fg": "#9D4EDD",
    "checkbox_hover": "#7B2CBF",
    "dropdown_bg": "#1A1A2E",
}


def Header_Title(Windows_cfg_autoDell):
    # Título
    Title = customtkinter.CTkLabel(
        Windows_cfg_autoDell,
        text="Configurar Auto Deletar".upper(),
        font=customtkinter.CTkFont(family="Consolas", size=20, weight="bold"),
        text_color=COLORS["text_primary"],
        anchor="center",
        justify="center",
    )
    Title.pack(side="top", fill="x", padx=10, pady=(10, 5))


def Enable_Disable_AutoDelete(Windows_cfg_autoDell, ext_frame):
    # Cria a variável booleana associada ao estado da configuração
    value_var = customtkinter.BooleanVar(value=config["AutoDelete"])

    def on_checkbox_toggle():
        # Quando o usuário clicar, pega o novo valor da variável e salva
        new_value = value_var.get()
        enable_obj = delete.AutoDelete(AutoDell=new_value)
        enable_obj.AutoDelete = enable_obj.AutoDelete
        # Altera de forma Dinâmica o texto de ativado e desativado
        if new_value:
            checkbox.configure(text="Auto Deletar Ativado")
            # Se ativou, mostra as opções
            ext_frame.pack(fill="x", padx=22, pady=(20, 20))
        else:
            checkbox.configure(text="Auto Deletar Desativado")
            # Se desativou, esconde as opções
            ext_frame.pack_forget()

    # Define o texto inicial dependendo da configuração atual
    texto_inicial = (
        "Auto Deletar Ativado" if config["AutoDelete"] else "Auto Deletar Desativado"
    )

    checkbox = customtkinter.CTkCheckBox(
        Windows_cfg_autoDell,
        text=texto_inicial,
        variable=value_var,
        font=customtkinter.CTkFont(family="Consolas", size=11),
        fg_color=COLORS["checkbox_fg"],
        hover_color=COLORS["checkbox_hover"],
        border_color=COLORS["border"],
        checkmark_color=COLORS["text_primary"],
        text_color=COLORS["text_primary"],
        width=120,
        corner_radius=4,
        command=on_checkbox_toggle,
    )
    checkbox.pack(side="top", padx=10, pady=8)


def save_filter_choice(selected_filter):
    # Reseta todos para false primeiro e true apenas pro selecionado
    for k, v in config["AutoDeleteConfig"].items():
        if k == "Dias para Auto Deletar":
            pass
        config["AutoDeleteConfig"][k] = False
    if selected_filter == "Dias para Auto Deletar":
        pass
    config["AutoDeleteConfig"][selected_filter] = True
    save_config("dist", "config", config)


def Select_Filter(ext_frame):
    filter_obj = delete.AutoDeleFilter().GetFilters()
    # Título da seção "Filtros de Exclusão"
    lbl_title_filter = customtkinter.CTkLabel(
        ext_frame,
        text="Filtros de Exclusão:",
        font=customtkinter.CTkFont(family="Consolas", size=15, weight="bold"),
        text_color=COLORS["accent_primary"],
    )
    lbl_title_filter.grid(
        row=0, column=0, columnspan=6, padx=10, pady=(15, 5), sticky="w"
    )

    for category, Filters in config.items():
        if category == "AutoDeleteConfig":
            if not isinstance(Filters, dict):
                continue

            row = 1
            col = 0
            max_cols = 3

            # Identificando qual opção já estava como 'True' no JSON pra iniciar a RadioVar com ela
            selected_option_str = ""
            for Filter_name, is_enabled in filter_obj.items():
                if is_enabled:
                    selected_option_str = Filter_name
                    break

            # Se ninguém estava selecionado antes (ou o dict mudou), assumir primeira chave
            if selected_option_str == "" and len(Filters) > 0:
                selected_option_str = list(Filters.keys())[0]

            # Variável de Radio controla as opções em formato de string
            radio_var = customtkinter.StringVar(value=selected_option_str)

            for Filter, enabled in Filters.items():
                if Filter == "Dias para Auto Deletar":
                    continue
                radio = customtkinter.CTkRadioButton(
                    ext_frame,
                    text=Filter,
                    value=Filter,
                    variable=radio_var,
                    font=customtkinter.CTkFont(family="Consolas", size=12),
                    fg_color=COLORS["checkbox_fg"],
                    hover_color=COLORS["checkbox_hover"],
                    border_color=COLORS["border"],
                    text_color=COLORS["text_primary"],
                    command=lambda f=Filter: delete.AutoDeleFilter.SetFilters(
                        None, f, True
                    ),
                )
                radio.grid(row=row, column=col, padx=10, pady=2, sticky="w")

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

                # Preenchendo buracos vazios na grid (se necessário)
                if col > 0:
                    for empty_col in range(col, max_cols):
                        spacer = customtkinter.CTkLabel(ext_frame, text="", width=120)
                        spacer.grid(row=row, column=empty_col)
        else:
            continue

    # Mostrar o frame de filtros apenas se o 'Ativa Auto Deletar' estiver True logo de início
    if config["AutoDelete"]:
        ext_frame.pack(fill="x", padx=22, pady=(10, 20))


def Time_AutoDelete(ext_frame):
    # Título da seção de Dias
    lbl_title_time = customtkinter.CTkLabel(
        ext_frame,
        text="Prazo para Exclusão:",
        font=customtkinter.CTkFont(family="Consolas", size=15, weight="bold"),
        text_color=COLORS["accent_primary"],
    )
    # A linha base começa depois das opções de rádio
    lbl_title_time.grid(
        row=4, column=0, columnspan=2, padx=10, pady=(35, 5), sticky="w"
    )

    # Adicionando um sub-container para o campo e texto de dias
    time_container = customtkinter.CTkFrame(ext_frame, fg_color="transparent")
    time_container.grid(
        row=5, column=0, columnspan=6, padx=10, pady=(10, 15), sticky="w"
    )

    time_value = config["AutoDeleteConfig"].get("Dias para Auto Deletar", "15")
    if time_value not in [
        "5",
        "10",
        "15",
        "20",
        "25",
        "30",
        "60",
        "120",
        "180",
        "240",
        "300",
        "360",
    ]:
        DropDownTimeValue = customtkinter.StringVar(value="15")
    else:
        DropDownTimeValue = customtkinter.StringVar(value=time_value)

    DropDown_time = customtkinter.CTkOptionMenu(
        time_container,
        fg_color=COLORS["dropdown_bg"],
        button_color=COLORS["accent_primary"],
        button_hover_color=COLORS["accent_hover"],
        text_color=COLORS["text_primary"],
        height=32,
        width=80,
        font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
        dropdown_fg_color=COLORS["dropdown_bg"],
        dropdown_text_color=COLORS["text_primary"],
        dropdown_hover_color=COLORS["accent_hover"],
        variable=DropDownTimeValue,
        command=lambda x: timeVerification.DaysAutoDelete(x).Setdays(),
        values=[
            "5",
            "10",
            "15",
            "20",
            "25",
            "30",
            "60",
            "120",
            "180",
            "240",
            "300",
            "360",
        ],
        dynamic_resizing=False,
        corner_radius=8,
    )
    DropDown_time.pack(side="left")

    description_time = customtkinter.CTkLabel(
        time_container,
        text="Dias para excluir o arquivo.",
        font=customtkinter.CTkFont(family="Segoe UI", size=12),
        text_color=COLORS["text_secondary"],
    )
    description_time.pack(side="left", padx=(10, 0))


def type_of_delete(ext_frame):
    row = 4
    col = 0
    filters_obj = delete.AutoDelete.GetFilters(None)
    Title_section = customtkinter.CTkLabel(
        ext_frame,
        text=f"Tipo de exclusão",
        font=customtkinter.CTkFont(family="Consolas", size=15, weight="bold"),
        text_color=COLORS["accent_primary"],
    )
    Title_section.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="sw")

    selected_option_str = ""
    for Filter_name, is_enabled in filters_obj.items():
        if Filter_name.startswith("Enviar Para Lixeira") or Filter_name.startswith(
            "Excluir permanentemente"
        ):
            print(is_enabled)
            if is_enabled:
                selected_option_str = Filter_name
                break

    radio_var = customtkinter.StringVar(value=selected_option_str)
    for tipo in filters_obj.keys():
        radio = customtkinter.CTkRadioButton(
            ext_frame,
            text=tipo,
            value=tipo,
            variable=radio_var,
            font=customtkinter.CTkFont(family="Consolas", size=12),
            fg_color=COLORS["checkbox_fg"],
            hover_color=COLORS["checkbox_hover"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            command=lambda f=tipo: delete.AutoDelete.SetFilters(None, f, True),
        )
        radio.grid(row=row, column=col, padx=(10, 5), pady=5, sticky="nw")

        col += 1


def open_Windows_CFG_autoDell(parent):
    global config
    config = load_config("dist", "config")
    icon_dir = os.path.join(os.path.dirname(__file__), "icon")
    icon_path = os.path.join(icon_dir, "IconApp.ico")

    # Configurações Auto Deletar
    Windows_cfg_autoDell = customtkinter.CTkToplevel(parent)
    if parent:
        Windows_cfg_autoDell.transient(parent)
    Windows_cfg_autoDell.title("Configurações Auto Deletar")
    Windows_cfg_autoDell.geometry("600x480")
    Windows_cfg_autoDell.resizable(False, False)
    Windows_cfg_autoDell.configure(bg_color=COLORS["bg_primary"])
    Windows_cfg_autoDell.grab_set()
    Centralizar_Janela(Windows_cfg_autoDell, 645, 370)
    Windows_cfg_autoDell.lift()
    Windows_cfg_autoDell.focus_force()
    Windows_cfg_autoDell.after(
        100, lambda: (Windows_cfg_autoDell.lift(), Windows_cfg_autoDell.focus_force())
    )
    Header_Title(Windows_cfg_autoDell)

    # Checkbox que ativa/desativa auto deletar
    cmd_frame = customtkinter.CTkFrame(
        master=Windows_cfg_autoDell, fg_color="transparent"
    )
    cmd_frame.pack(fill="x", padx=40, pady=(10, 0))

    # Criamos o Frame onde as opções moram
    ext_frame = customtkinter.CTkFrame(
        master=Windows_cfg_autoDell,
        fg_color=COLORS["bg_secondary"],
        corner_radius=10,
        width=600,
        height=600,
    )

    # Passamos os frames apropriados para não empurrar a grid errada
    Enable_Disable_AutoDelete(cmd_frame, ext_frame)
    Select_Filter(ext_frame)
    type_of_delete(ext_frame)
    Time_AutoDelete(ext_frame)

    if parent is None:
        Windows_cfg_autoDell.mainloop()

    try:
        if os.path.exists(icon_path):
            Windows_cfg_autoDell.after(
                200, lambda: Windows_cfg_autoDell.iconbitmap(icon_path)
            )
    except Exception:
        pass

    config = load_config("dist", "config")


if __name__ == "__main__":
    open_Windows_CFG_autoDell(None)
