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
from utils.translate import Translate

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
    "button_secondary": "#2D2D44",
    "button_secondary_hover": "#3D3D54",
}


def Header_Title(Windows_cfg_autoDell):
    t = Translate()
    title_text = t.get_text("auto_delete", "title") or "Configurar Auto Deletar"
    Title = customtkinter.CTkLabel(
        Windows_cfg_autoDell,
        text=title_text.upper(),
        font=customtkinter.CTkFont(family="Consolas", size=20, weight="bold"),
        text_color=COLORS["text_primary"],
        anchor="center",
        justify="center",
    )
    Title.pack(side="top", fill="x", padx=10, pady=(15, 5))
    return Title


def Enable_Disable_AutoDelete(parent_frame, ext_frame):
    t = Translate()
    config = load_config("dist", "config")
    value_var = customtkinter.BooleanVar(value=config.get("AutoDelete", False))

    def on_checkbox_toggle():
        tr = Translate()
        new_value = value_var.get()
        enable_obj = delete.AutoDelete(AutoDell=new_value)
        enable_obj.AutoDelete = new_value
        if new_value:
            checkbox.configure(text=tr.get_text("auto_delete", "enabled") or "Auto Deletar Ativado")
            ext_frame.pack(fill="x", padx=15, pady=(15, 10))
        else:
            checkbox.configure(text=tr.get_text("auto_delete", "disabled") or "Auto Deletar Desativado")
            ext_frame.pack_forget()

    texto_ativo = t.get_text("auto_delete", "enabled") or "Auto Deletar Ativado"
    texto_inativo = t.get_text("auto_delete", "disabled") or "Auto Deletar Desativado"
    texto_inicial = texto_ativo if config.get("AutoDelete", False) else texto_inativo

    checkbox = customtkinter.CTkCheckBox(
        parent_frame,
        text=texto_inicial,
        variable=value_var,
        font=customtkinter.CTkFont(family="Consolas", size=12),
        fg_color=COLORS["checkbox_fg"],
        hover_color=COLORS["checkbox_hover"],
        border_color=COLORS["border"],
        checkmark_color=COLORS["text_primary"],
        text_color=COLORS["text_primary"],
        width=120,
        corner_radius=4,
        command=on_checkbox_toggle,
    )
    checkbox.pack(side="top", anchor="w", padx=10, pady=8)
    return checkbox


def Select_Filter(ext_frame):
    t = Translate()
    config = load_config("dist", "config")
    filter_obj = delete.AutoDeleFilter().GetFilters()

    lbl_title_filter = customtkinter.CTkLabel(
        ext_frame,
        text=t.get_text("auto_delete", "filters_title") or "Filtros de Exclusão:",
        font=customtkinter.CTkFont(family="Consolas", size=14, weight="bold"),
        text_color=COLORS["accent_primary"],
    )
    lbl_title_filter.grid(
        row=0, column=0, columnspan=6, padx=15, pady=(12, 5), sticky="w"
    )

    filters_dict = config.get("AutoDeleteConfig", {})
    selected_option_str = ""
    for Filter_name, is_enabled in filter_obj.items():
        if is_enabled:
            selected_option_str = Filter_name
            break

    if selected_option_str == "" and len(filters_dict) > 0:
        for k in filters_dict:
            if k != "Dias para Auto Deletar":
                selected_option_str = k
                break

    radio_var = customtkinter.StringVar(value=selected_option_str)
    col = 0
    row = 1
    filter_labels = [
        (
            "Por Data de Criação",
            t.get_text("auto_delete", "filter_create_date")
            or "Por Data de Criação",
        ),
        (
            "Por Data de Modificação",
            t.get_text("auto_delete", "filter_modify_date")
            or "Por Data de Modificação",
        ),
    ]
    for Filter_key, Filter_label in filter_labels:
        if Filter_key in filters_dict:
            radio = customtkinter.CTkRadioButton(
                ext_frame,
                text=Filter_label,
                value=Filter_key,
                variable=radio_var,
                font=customtkinter.CTkFont(family="Consolas", size=12),
                fg_color=COLORS["checkbox_fg"],
                hover_color=COLORS["checkbox_hover"],
                border_color=COLORS["border"],
                text_color=COLORS["text_primary"],
                command=lambda f=Filter_key: delete.AutoDeleFilter.SetFilters(
                    None, f, True
                ),
            )
            radio.grid(row=row, column=col, padx=(15, 20), pady=4, sticky="w")
            col += 1


def Time_AutoDelete(ext_frame):
    t = Translate()
    config = load_config("dist", "config")
    lbl_title_time = customtkinter.CTkLabel(
        ext_frame,
        text=t.get_text("auto_delete", "time_title") or "Prazo para Exclusão:",
        font=customtkinter.CTkFont(family="Consolas", size=14, weight="bold"),
        text_color=COLORS["accent_primary"],
    )
    lbl_title_time.grid(
        row=4, column=0, columnspan=2, padx=15, pady=(15, 5), sticky="w"
    )

    time_container = customtkinter.CTkFrame(ext_frame, fg_color="transparent")
    time_container.grid(
        row=5, column=0, columnspan=6, padx=15, pady=(5, 15), sticky="w"
    )

    time_value = config.get("AutoDeleteConfig", {}).get("Dias para Auto Deletar", "15")
    valid_values = [
        "5", "10", "15", "20", "25", "30", "60", "120", "180", "240", "300", "360"
    ]
    if time_value not in valid_values:
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
        values=valid_values,
        dynamic_resizing=False,
        corner_radius=8,
    )
    DropDown_time.pack(side="left")

    description_time = customtkinter.CTkLabel(
        time_container,
        text=t.get_text("auto_delete", "days") or "Dias para excluir o arquivo.",
        font=customtkinter.CTkFont(family="Segoe UI", size=12),
        text_color=COLORS["text_secondary"],
    )
    description_time.pack(side="left", padx=(10, 0))


def type_of_delete(ext_frame):
    t = Translate()
    filters_obj = delete.AutoDelete.GetFilters(None)
    Title_section = customtkinter.CTkLabel(
        ext_frame,
        text=t.get_text("auto_delete", "type_of_delete") or "Tipo de exclusão",
        font=customtkinter.CTkFont(family="Consolas", size=14, weight="bold"),
        text_color=COLORS["accent_primary"],
    )
    Title_section.grid(row=2, column=0, padx=15, pady=(15, 5), sticky="w")

    selected_option_str = ""
    for Filter_name, is_enabled in filters_obj.items():
        if is_enabled:
            selected_option_str = Filter_name
            break

    if not selected_option_str:
        selected_option_str = "Enviar Para Lixeira"

    radio_var = customtkinter.StringVar(value=selected_option_str)
    col = 0
    type_labels = [
        (
            "Enviar Para Lixeira",
            t.get_text("auto_delete", "type_2") or "Enviar para a lixeira",
        ),
        (
            "Excluir permanentemente",
            t.get_text("auto_delete", "type_1") or "Excluir permanentemente",
        ),
    ]
    for tipo_key, tipo_label in type_labels:
        radio = customtkinter.CTkRadioButton(
            ext_frame,
            text=tipo_label,
            value=tipo_key,
            variable=radio_var,
            font=customtkinter.CTkFont(family="Consolas", size=12),
            fg_color=COLORS["checkbox_fg"],
            hover_color=COLORS["checkbox_hover"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            command=lambda f=tipo_key: delete.AutoDelete.SetFilters(None, f, True),
        )
        radio.grid(row=3, column=col, padx=(15, 20), pady=4, sticky="w")
        col += 1


# --- Funções de exclusão de pastas ---

def Enable_Disable_Folder_Delete(parent_frame, ext_frame):
    t = Translate()
    folder_del_obj = delete.Folder_Delete()
    is_active = folder_del_obj.GetAtivado
    value_var = customtkinter.BooleanVar(value=is_active)

    def on_checkbox_toggle():
        tr = Translate()
        new_value = value_var.get()
        folder_del_obj.Ativado = new_value
        if new_value:
            checkbox.configure(
                text=tr.get_text("auto_delete", "folder_enabled") or "Auto Deletar Pastas Ativado"
            )
            ext_frame.pack(fill="x", padx=15, pady=(15, 10))
        else:
            checkbox.configure(
                text=tr.get_text("auto_delete", "folder_disabled") or "Auto Deletar Pastas Desativado"
            )
            ext_frame.pack_forget()

    texto_ativo = t.get_text("auto_delete", "folder_enabled") or "Auto Deletar Pastas Ativado"
    texto_inativo = t.get_text("auto_delete", "folder_disabled") or "Auto Deletar Pastas Desativado"
    texto_inicial = texto_ativo if is_active else texto_inativo

    checkbox = customtkinter.CTkCheckBox(
        parent_frame,
        text=texto_inicial,
        variable=value_var,
        font=customtkinter.CTkFont(family="Consolas", size=12),
        fg_color=COLORS["checkbox_fg"],
        hover_color=COLORS["checkbox_hover"],
        border_color=COLORS["border"],
        checkmark_color=COLORS["text_primary"],
        text_color=COLORS["text_primary"],
        width=120,
        corner_radius=4,
        command=on_checkbox_toggle,
    )
    checkbox.pack(side="top", anchor="w", padx=10, pady=8)
    return checkbox


def Folder_Delete_Type(ext_frame):
    t = Translate()
    folder_del_obj = delete.Folder_Delete()
    filters_obj = folder_del_obj.GetFilters()

    Title_section = customtkinter.CTkLabel(
        ext_frame,
        text=t.get_text("auto_delete", "type_of_delete") or "Tipo de exclusão",
        font=customtkinter.CTkFont(family="Consolas", size=14, weight="bold"),
        text_color=COLORS["accent_primary"],
    )
    Title_section.grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")

    if filters_obj.get("excluir_permanentemente", False):
        selected_type = "excluir_permanentemente"
    else:
        selected_type = "lixeira"

    radio_var = customtkinter.StringVar(value=selected_type)

    radio_trash = customtkinter.CTkRadioButton(
        ext_frame,
        text=t.get_text("auto_delete", "type_2") or "Enviar para a lixeira",
        value="lixeira",
        variable=radio_var,
        font=customtkinter.CTkFont(family="Consolas", size=12),
        fg_color=COLORS["checkbox_fg"],
        hover_color=COLORS["checkbox_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_primary"],
        command=lambda: folder_del_obj.SetFilters("lixeira", True),
    )
    radio_trash.grid(row=1, column=0, padx=(15, 20), pady=4, sticky="w")

    radio_perma = customtkinter.CTkRadioButton(
        ext_frame,
        text=t.get_text("auto_delete", "type_1") or "Excluir permanentemente",
        value="excluir_permanentemente",
        variable=radio_var,
        font=customtkinter.CTkFont(family="Consolas", size=12),
        fg_color=COLORS["checkbox_fg"],
        hover_color=COLORS["checkbox_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_primary"],
        command=lambda: folder_del_obj.SetFilters("excluir_permanentemente", True),
    )
    radio_perma.grid(row=1, column=1, padx=(15, 20), pady=4, sticky="w")


def Folder_Delete_Scope(ext_frame):
    t = Translate()
    folder_del_obj = delete.Folder_Delete()
    filters_obj = folder_del_obj.GetFilters()

    Title_section = customtkinter.CTkLabel(
        ext_frame,
        text=t.get_text("auto_delete", "folder_scope_title") or "Escopo de Exclusão de Pastas:",
        font=customtkinter.CTkFont(family="Consolas", size=14, weight="bold"),
        text_color=COLORS["accent_primary"],
    )
    Title_section.grid(row=2, column=0, padx=15, pady=(15, 5), sticky="w")

    if filters_obj.get("pastas_ORZ", False):
        selected_scope = "pastas_ORZ"
    else:
        selected_scope = "todas"

    radio_var = customtkinter.StringVar(value=selected_scope)

    radio_all = customtkinter.CTkRadioButton(
        ext_frame,
        text=t.get_text("auto_delete", "folder_scope_all") or "Todas as Pastas Vazias",
        value="todas",
        variable=radio_var,
        font=customtkinter.CTkFont(family="Consolas", size=12),
        fg_color=COLORS["checkbox_fg"],
        hover_color=COLORS["checkbox_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_primary"],
        command=lambda: folder_del_obj.SetFilters("todas", True),
    )
    radio_all.grid(row=3, column=0, padx=(15, 20), pady=4, sticky="w")

    radio_orz = customtkinter.CTkRadioButton(
        ext_frame,
        text=t.get_text("auto_delete", "folder_scope_orz") or "Apenas Pastas do FileORZ",
        value="pastas_ORZ",
        variable=radio_var,
        font=customtkinter.CTkFont(family="Consolas", size=12),
        fg_color=COLORS["checkbox_fg"],
        hover_color=COLORS["checkbox_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_primary"],
        command=lambda: folder_del_obj.SetFilters("pastas_ORZ", True),
    )
    radio_orz.grid(row=3, column=1, padx=(15, 20), pady=4, sticky="w")


def Folder_Delete_Info(ext_frame):
    t = Translate()
    lbl_desc = customtkinter.CTkLabel(
        ext_frame,
        text=t.get_text("auto_delete", "folder_desc") or "Remove automaticamente pastas vazias no diretório de organização.",
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color=COLORS["text_secondary"],
        justify="left",
        wraplength=520,
    )
    lbl_desc.grid(row=4, column=0, columnspan=2, padx=15, pady=(15, 15), sticky="w")


def open_Windows_CFG_autoDell(parent):
    t = Translate()
    icon_dir = os.path.join(os.path.dirname(__file__), "icon")
    icon_path = os.path.join(icon_dir, "IconApp.ico")

    Windows_cfg_autoDell = customtkinter.CTkToplevel(parent)
    if parent:
        Windows_cfg_autoDell.transient(parent)
    Windows_cfg_autoDell.title(
        t.get_text("auto_delete", "Window_tittle") or "Configurações Auto Deletar"
    )
    Windows_cfg_autoDell.geometry("660x460")
    Windows_cfg_autoDell.resizable(False, False)
    Windows_cfg_autoDell.configure(fg_color=COLORS["bg_primary"])
    Windows_cfg_autoDell.grab_set()
    Centralizar_Janela(Windows_cfg_autoDell, 660, 460)
    Windows_cfg_autoDell.lift()
    Windows_cfg_autoDell.focus_force()
    Windows_cfg_autoDell.after(
        100, lambda: (Windows_cfg_autoDell.lift(), Windows_cfg_autoDell.focus_force())
    )

    header_title = Header_Title(Windows_cfg_autoDell)

    tabview = customtkinter.CTkTabview(
        Windows_cfg_autoDell,
        fg_color=COLORS["bg_primary"],
        segmented_button_fg_color=COLORS["bg_secondary"],
        segmented_button_selected_color=COLORS["accent_primary"],
        segmented_button_selected_hover_color=COLORS["accent_hover"],
        segmented_button_unselected_color=COLORS["button_secondary"],
        segmented_button_unselected_hover_color=COLORS["button_secondary_hover"],
        text_color=COLORS["text_primary"],
    )
    tabview.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    tab_files_title = t.get_text("auto_delete", "tab_files") or "📄 Arquivos"
    tab_folders_title = t.get_text("auto_delete", "tab_folders") or "📁 Pastas"

    tab_files = tabview.add(tab_files_title)
    tab_folders = tabview.add(tab_folders_title)

    # --- Configuração da aba Arquivos ---
    config_current = load_config("dist", "config")
    cmd_frame_files = customtkinter.CTkFrame(tab_files, fg_color="transparent")
    cmd_frame_files.pack(fill="x", padx=15, pady=(10, 0))

    ext_frame_files = customtkinter.CTkFrame(
        tab_files,
        fg_color=COLORS["bg_secondary"],
        corner_radius=10,
    )

    Enable_Disable_AutoDelete(cmd_frame_files, ext_frame_files)
    Select_Filter(ext_frame_files)
    type_of_delete(ext_frame_files)
    Time_AutoDelete(ext_frame_files)

    if config_current.get("AutoDelete", False):
        ext_frame_files.pack(fill="x", padx=15, pady=(15, 10))

    # --- Configuração da aba Pastas ---
    folder_del_current = delete.Folder_Delete()
    cmd_frame_folders = customtkinter.CTkFrame(tab_folders, fg_color="transparent")
    cmd_frame_folders.pack(fill="x", padx=15, pady=(10, 0))

    ext_frame_folders = customtkinter.CTkFrame(
        tab_folders,
        fg_color=COLORS["bg_secondary"],
        corner_radius=10,
    )

    Enable_Disable_Folder_Delete(cmd_frame_folders, ext_frame_folders)
    Folder_Delete_Type(ext_frame_folders)
    Folder_Delete_Scope(ext_frame_folders)
    Folder_Delete_Info(ext_frame_folders)

    if folder_del_current.GetAtivado:
        ext_frame_folders.pack(fill="x", padx=15, pady=(15, 10))

    def update_texts():
        tr = Translate()
        if not Windows_cfg_autoDell.winfo_exists():
            return
        Windows_cfg_autoDell.title(
            tr.get_text("auto_delete", "Window_tittle") or "Configurações Auto Deletar"
        )
        header_title.configure(
            text=(tr.get_text("auto_delete", "title") or "Configurar Auto Deletar").upper()
        )

    Translate.register_listener(update_texts)

    def on_close():
        Translate.unregister_listener(update_texts)
        Windows_cfg_autoDell.destroy()

    Windows_cfg_autoDell.protocol("WM_DELETE_WINDOW", on_close)

    try:
        if os.path.exists(icon_path):
            Windows_cfg_autoDell.after(
                200, lambda: Windows_cfg_autoDell.iconbitmap(icon_path)
            )
    except Exception:
        pass

    if parent is None:
        Windows_cfg_autoDell.mainloop()


if __name__ == "__main__":
    open_Windows_CFG_autoDell(None)
