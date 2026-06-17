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
from ui.Centralizar_Janela import Centralizar_Janela

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import load_config, save_config
from utils.AdvancedConfig import AdvancedConfig
from utils import delete, timeVerification

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


def open_config_window(parent):
    icon_dir = os.path.join(os.path.dirname(__file__), "icon")
    icon_path = os.path.join(icon_dir, "IconApp.ico")

    window = customtkinter.CTkToplevel(parent)
    window.title("Configurações Gerais - FileORZ")
    window.geometry("900x700")
    window.configure(fg_color=COLORS["bg_primary"])
    window.resizable(False, False)
    window.grab_set()
    Centralizar_Janela(window, 900, 700)

    try:
        if os.path.exists(icon_path):
            window.after(200, lambda: window.iconbitmap(icon_path))
    except Exception:
        pass

    # Header Geral da Janela de Configurações
    header_frame = customtkinter.CTkFrame(
        window, fg_color="#1E1E3F", corner_radius=0, height=65
    )
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    header_inner = customtkinter.CTkFrame(header_frame, fg_color="transparent")
    header_inner.pack(fill="both", expand=True, padx=25, pady=12)

    header_icon = customtkinter.CTkLabel(
        header_inner, text="⚙️", font=customtkinter.CTkFont(size=22)
    )
    header_icon.pack(side="left")

    header_title = customtkinter.CTkLabel(
        header_inner,
        text="Configuração - FileORZ",
        font=customtkinter.CTkFont(family="Segoe UI", size=18, weight="bold"),
        text_color=COLORS["text_primary"],
    )
    header_title.pack(side="left", padx=(10, 0))

    header_subtitle = customtkinter.CTkLabel(
        header_inner,
        text="Ajuste as preferências do organizador",
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color=COLORS["text_secondary"],
    )
    header_subtitle.pack(side="right")

    # Criando o Tabview para separar as seções
    tabview = customtkinter.CTkTabview(
        window,
        fg_color=COLORS["bg_primary"],
        segmented_button_fg_color=COLORS["bg_secondary"],
        segmented_button_selected_color=COLORS["accent_primary"],
        segmented_button_selected_hover_color=COLORS["accent_hover"],
        segmented_button_unselected_color=COLORS["bg_secondary"],
        segmented_button_unselected_hover_color=COLORS["button_secondary_hover"],
        text_color=COLORS["text_primary"],
    )
    tabview.pack(fill="both", expand=True, padx=15, pady=(10, 15))

    tab_extensions = tabview.add("📁 Categorias e Extensões")
    tab_advanced = tabview.add("🧠 Organização Avançada")
    tab_autodelete = tabview.add("🗑️ Auto Deletar")

    config = load_config("dist", "config")
    extension_vars = {}

    scroll_frame = customtkinter.CTkScrollableFrame(
        tab_extensions,
        width=840,
        height=440,
        fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["accent_primary"],
        scrollbar_button_hover_color=COLORS["accent_hover"],
    )
    scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

    for category, extensions in config.items():
        if (
            category == "Folder"
            or category == "AutoDelete"
            or category == "AutoDeleteConfig"
        ):
            continue

        if not isinstance(extensions, dict):
            continue

        extension_vars[category] = {}

        cat_frame = customtkinter.CTkFrame(
            scroll_frame,
            fg_color=COLORS["bg_secondary"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        cat_frame.pack(pady=8, padx=5, fill="x")

        header_container = customtkinter.CTkFrame(cat_frame, fg_color="transparent")
        header_container.pack(fill="x", padx=18, pady=(15, 10))

        cat_left = customtkinter.CTkFrame(header_container, fg_color="transparent")
        cat_left.pack(side="left")

        cat_icon = customtkinter.CTkLabel(
            cat_left, text="📁", font=customtkinter.CTkFont(size=16)
        )
        cat_icon.pack(side="left")

        cat_label = customtkinter.CTkLabel(
            cat_left,
            text=category.upper(),
            font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLORS["text_category"],
        )
        cat_label.pack(side="left", padx=(8, 0))

        enabled_count = sum(1 for v in extensions.values() if v)
        total_count = len(extensions)
        count_label = customtkinter.CTkLabel(
            cat_left,
            text=f"  •  {enabled_count}/{total_count} selecionadas",
            font=customtkinter.CTkFont(family="Segoe UI", size=11),
            text_color=COLORS["text_secondary"],
        )
        count_label.pack(side="left")

        cat_right = customtkinter.CTkFrame(header_container, fg_color="transparent")
        cat_right.pack(side="right")

        def select_all(cat=category):
            for ext_var in extension_vars[cat].values():
                ext_var.set(True)

        def deselect_all(cat=category):
            for ext_var in extension_vars[cat].values():
                ext_var.set(False)

        btn_select_all = customtkinter.CTkButton(
            cat_right,
            text="✓ Todos",
            command=select_all,
            fg_color=COLORS["accent_success"],
            hover_color=COLORS["accent_success_hover"],
            font=customtkinter.CTkFont(family="Segoe UI", size=11, weight="bold"),
            width=80,
            height=28,
            corner_radius=6,
        )
        btn_select_all.pack(side="left", padx=(0, 8))

        btn_deselect_all = customtkinter.CTkButton(
            cat_right,
            text="✗ Nenhum",
            command=deselect_all,
            fg_color=COLORS["accent_danger"],
            hover_color=COLORS["accent_danger_hover"],
            font=customtkinter.CTkFont(family="Segoe UI", size=11, weight="bold"),
            width=90,
            height=28,
            corner_radius=6,
        )
        btn_deselect_all.pack(side="left")

        ext_frame = customtkinter.CTkFrame(
            cat_frame, fg_color=COLORS["bg_card_inner"], corner_radius=8
        )
        ext_frame.pack(fill="x", padx=18, pady=(5, 18))

        row_idx = 0
        col_idx = 0
        max_cols = 6

        for ext, enabled in extensions.items():
            var = customtkinter.BooleanVar(value=enabled)
            extension_vars[category][ext] = var

            checkbox = customtkinter.CTkCheckBox(
                ext_frame,
                text=ext,
                variable=var,
                font=customtkinter.CTkFont(family="Consolas", size=11),
                fg_color=COLORS["checkbox_fg"],
                hover_color=COLORS["checkbox_hover"],
                border_color=COLORS["border"],
                checkmark_color=COLORS["text_primary"],
                text_color=COLORS["text_primary"],
                width=120,
                corner_radius=4,
            )
            checkbox.grid(row=row_idx, column=col_idx, padx=10, pady=8, sticky="w")

            col_idx += 1
            if col_idx >= max_cols:
                col_idx = 0
                row_idx += 1

        if col_idx > 0:
            for empty_col in range(col_idx, max_cols):
                spacer = customtkinter.CTkLabel(ext_frame, text="", width=120)
                spacer.grid(row=row_idx, column=empty_col)

    # Footer da Aba 1 (Botão Salvar específico)
    footer_frame = customtkinter.CTkFrame(
        tab_extensions, fg_color=COLORS["bg_secondary"], height=60, corner_radius=10
    )
    footer_frame.pack(fill="x", side="bottom", pady=(5, 5))
    footer_frame.pack_propagate(False)

    footer_inner = customtkinter.CTkFrame(footer_frame, fg_color="transparent")
    footer_inner.pack(fill="both", expand=True, padx=15, pady=10)

    feedback_container = customtkinter.CTkFrame(footer_inner, fg_color="transparent")
    feedback_container.pack(side="left", fill="y")

    def save_changes():
        config_data = load_config("dist", "config")

        for category, exts in extension_vars.items():
            if category in config_data:
                for ext, var in exts.items():
                    config_data[category][ext] = var.get()

        save_config("dist", "config", config_data)

        success_label = customtkinter.CTkLabel(
            feedback_container,
            text="✓  Configurações salvas com sucesso!",
            font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=COLORS["accent_success"],
        )
        success_label.pack(side="left", anchor="center")
        window.after(2500, success_label.destroy)

    save_button = customtkinter.CTkButton(
        footer_inner,
        text="💾  Salvar Categorias",
        command=save_changes,
        fg_color=COLORS["accent_primary"],
        hover_color=COLORS["accent_hover"],
        font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
        width=200,
        height=40,
        corner_radius=8,
    )
    save_button.pack(side="right")

    # ==========================================
    # ABA 2: ORGANIZAÇÃO AVANÇADA
    # ==========================================
    adv_config = AdvancedConfig()

    control_frame = customtkinter.CTkFrame(tab_advanced, fg_color="transparent")
    control_frame.pack(fill="x", padx=15, pady=10)

    advanced_var = customtkinter.BooleanVar(value=adv_config.get_enabled())

    def toggle_advanced():
        adv_config.set_enabled(advanced_var.get())
        if advanced_var.get():
            checkbox.configure(text="Modo Avançado Ativado")
        else:
            checkbox.configure(text="Modo Avançado Desativado")

    checkbox_text = (
        "Modo Avançado Ativado" if advanced_var.get() else "Modo Avançado Desativado"
    )
    checkbox = customtkinter.CTkCheckBox(
        control_frame,
        text=checkbox_text,
        variable=advanced_var,
        command=toggle_advanced,
        font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
        fg_color=COLORS["checkbox_fg"],
        hover_color=COLORS["checkbox_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_primary"],
    )
    checkbox.pack(side="left")

    def add_group():
        keywords_data = adv_config.load_keywords()
        if "" not in keywords_data:
            new_data = {"": []}
            new_data.update(keywords_data)
            adv_config.save_keywords(new_data)
            refresh_keywords()

    btn_add = customtkinter.CTkButton(
        control_frame,
        text="+ Adicionar Grupo",
        command=add_group,
        fg_color=COLORS["accent_success"],
        hover_color=COLORS["accent_success_hover"],
        font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
        width=150,
        height=35,
        corner_radius=8,
    )
    btn_add.pack(side="right")

    description = customtkinter.CTkLabel(
        tab_advanced,
        text="Defina o nome do grupo e as palavras-chave (separadas por vírgula) para organizar seus PDFs.\n"
        "Clique no ícone de salvar em cada card para aplicar as alterações.",
        font=customtkinter.CTkFont(family="Segoe UI", size=12),
        text_color=COLORS["text_secondary"],
        justify="left",
    )
    description.pack(padx=15, pady=(0, 10), anchor="w")

    keywords_scroll = customtkinter.CTkScrollableFrame(
        tab_advanced,
        fg_color=COLORS["bg_secondary"],
        border_width=1,
        border_color=COLORS["border"],
        corner_radius=12,
    )
    keywords_scroll.pack(fill="both", expand=True, padx=15, pady=(10, 10))

    def refresh_keywords():
        for widget in keywords_scroll.winfo_children():
            widget.destroy()

        keywords_data = adv_config.load_keywords()

        if not keywords_data and "" not in keywords_data:
            empty_label = customtkinter.CTkLabel(
                keywords_scroll,
                text="Nenhum grupo cadastrado. Clique em + Adicionar Grupo.",
                font=customtkinter.CTkFont(family="Segoe UI", size=14),
                text_color=COLORS["text_secondary"],
            )
            empty_label.pack(pady=50)
            return

        for category, words in keywords_data.items():
            group_card = customtkinter.CTkFrame(
                keywords_scroll,
                fg_color=COLORS["bg_card"],
                corner_radius=10,
                border_width=1,
                border_color=COLORS["border"],
            )
            group_card.pack(fill="x", padx=10, pady=8)

            card_header = customtkinter.CTkFrame(group_card, fg_color="transparent")
            card_header.pack(fill="x", padx=15, pady=(10, 5))

            name_entry = customtkinter.CTkEntry(
                card_header,
                placeholder_text="Nome do Grupo (ex: Boletos)",
                font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
                fg_color="transparent",
                border_width=1,
                border_color=COLORS["border"],
                text_color=COLORS["accent_primary"],
                width=300,
            )
            if category:
                name_entry.insert(0, category)
            name_entry.pack(side="left")

            def delete_group(cat=category):
                data = adv_config.load_keywords()
                if cat in data:
                    del data[cat]
                    adv_config.save_keywords(data)
                    refresh_keywords()

            btn_del = customtkinter.CTkButton(
                card_header,
                text="🗑️".replace("\ufe0f", "").replace("\u200b", "").strip(),
                width=35,
                height=30,
                fg_color=COLORS["accent_danger"],
                hover_color=COLORS["accent_danger_hover"],
                command=delete_group,
                corner_radius=6,
            )
            btn_del.pack(side="right")

            input_frame = customtkinter.CTkFrame(group_card, fg_color="transparent")
            input_frame.pack(fill="x", padx=15, pady=(0, 15))

            words_text = ", ".join(words)
            words_entry = customtkinter.CTkEntry(
                input_frame,
                placeholder_text="Palavras ou frases separadas por vírgula...",
                font=customtkinter.CTkFont(family="Segoe UI", size=12),
                fg_color=COLORS["bg_card_inner"],
                border_color=COLORS["border"],
                height=35,
            )
            if words_text:
                words_entry.insert(0, words_text)
            words_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

            def save_group(old_cat=category, n_entry=name_entry, w_entry=words_entry):
                new_cat = n_entry.get().strip()
                if not new_cat:
                    n_entry.configure(
                        border_width=1, border_color=COLORS["accent_danger"]
                    )
                    return

                new_words = [w.strip() for w in w_entry.get().split(",") if w.strip()]

                data = adv_config.load_keywords()

                if old_cat in data:
                    del data[old_cat]

                data[new_cat] = new_words
                adv_config.save_keywords(data)

                n_entry.configure(border_width=0)
                w_entry.configure(border_color=COLORS["accent_success"])
                window.after(500, refresh_keywords)

            btn_save = customtkinter.CTkButton(
                input_frame,
                text="💾",
                width=35,
                height=35,
                fg_color=COLORS["accent_primary"],
                hover_color=COLORS["accent_hover"],
                command=save_group,
                corner_radius=6,
            )
            btn_save.pack(side="right")

    refresh_keywords()

    # ==========================================
    # ABA 3: AUTO DELETAR
    # ==========================================
    autodelete_content = customtkinter.CTkFrame(tab_autodelete, fg_color="transparent")
    autodelete_content.pack(fill="both", expand=True, padx=15, pady=10)

    autodelete_config = load_config("dist", "config")
    value_var_ad = customtkinter.BooleanVar(
        value=autodelete_config.get("AutoDelete", False)
    )

    options_frame_ad = customtkinter.CTkFrame(
        autodelete_content,
        fg_color=COLORS["bg_secondary"],
        corner_radius=12,
        border_width=1,
        border_color=COLORS["border"],
    )

    def on_checkbox_toggle_ad():
        new_value = value_var_ad.get()
        enable_obj = delete.AutoDelete(AutoDell=new_value)
        enable_obj.AutoDelete = enable_obj.AutoDelete

        if new_value:
            checkbox_ad.configure(text="Auto Deletar Ativado")
            options_frame_ad.pack(fill="x", pady=(15, 0), padx=5)
        else:
            checkbox_ad.configure(text="Auto Deletar Desativado")
            options_frame_ad.pack_forget()

    texto_inicial_ad = (
        "Auto Deletar Ativado"
        if autodelete_config.get("AutoDelete", False)
        else "Auto Deletar Desativado"
    )
    checkbox_ad = customtkinter.CTkCheckBox(
        autodelete_content,
        text=texto_inicial_ad,
        variable=value_var_ad,
        command=on_checkbox_toggle_ad,
        font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
        fg_color=COLORS["checkbox_fg"],
        hover_color=COLORS["checkbox_hover"],
        border_color=COLORS["border"],
        text_color=COLORS["text_primary"],
    )
    checkbox_ad.pack(anchor="w", padx=5)

    if autodelete_config.get("AutoDelete", False):
        options_frame_ad.pack(fill="x", pady=(15, 0), padx=5)

    # 1. Filtros de Exclusão
    filter_section_ad = customtkinter.CTkFrame(options_frame_ad, fg_color="transparent")
    filter_section_ad.pack(fill="x", padx=20, pady=15)

    lbl_title_filter_ad = customtkinter.CTkLabel(
        filter_section_ad,
        text="Filtros de Exclusão",
        font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
        text_color=COLORS["accent_primary"],
    )
    lbl_title_filter_ad.pack(anchor="w", pady=(0, 8))

    filter_options_ad = customtkinter.CTkFrame(
        filter_section_ad, fg_color="transparent"
    )
    filter_options_ad.pack(fill="x")

    filter_obj_ad = delete.AutoDeleFilter().GetFilters()
    selected_option_str_ad = ""
    for Filter_name, is_enabled in filter_obj_ad.items():
        if is_enabled:
            selected_option_str_ad = Filter_name
            break
    if selected_option_str_ad == "" and len(filter_obj_ad) > 0:
        selected_option_str_ad = list(filter_obj_ad.keys())[0]

    radio_var_filter_ad = customtkinter.StringVar(value=selected_option_str_ad)

    for Filter in filter_obj_ad.keys():
        radio = customtkinter.CTkRadioButton(
            filter_options_ad,
            text=Filter,
            value=Filter,
            variable=radio_var_filter_ad,
            font=customtkinter.CTkFont(family="Segoe UI", size=12),
            fg_color=COLORS["checkbox_fg"],
            hover_color=COLORS["checkbox_hover"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            command=lambda f=Filter: delete.AutoDeleFilter.SetFilters(None, f, True),
        )
        radio.pack(side="left", padx=(0, 30))

    # 2. Tipo de Exclusão
    delete_type_section_ad = customtkinter.CTkFrame(
        options_frame_ad, fg_color="transparent"
    )
    delete_type_section_ad.pack(fill="x", padx=20, pady=15)

    lbl_title_del_type_ad = customtkinter.CTkLabel(
        delete_type_section_ad,
        text="Tipo de Exclusão",
        font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
        text_color=COLORS["accent_primary"],
    )
    lbl_title_del_type_ad.pack(anchor="w", pady=(0, 8))

    del_type_options_ad = customtkinter.CTkFrame(
        delete_type_section_ad, fg_color="transparent"
    )
    del_type_options_ad.pack(fill="x")

    filters_obj_ad = delete.AutoDelete.GetFilters(None)
    selected_del_type_ad = ""
    for Filter_name, is_enabled in filters_obj_ad.items():
        if is_enabled:
            selected_del_type_ad = Filter_name
            break

    radio_var_del_type_ad = customtkinter.StringVar(value=selected_del_type_ad)

    for tipo in filters_obj_ad.keys():
        radio = customtkinter.CTkRadioButton(
            del_type_options_ad,
            text=tipo,
            value=tipo,
            variable=radio_var_del_type_ad,
            font=customtkinter.CTkFont(family="Segoe UI", size=12),
            fg_color=COLORS["checkbox_fg"],
            hover_color=COLORS["checkbox_hover"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            command=lambda f=tipo: delete.AutoDelete.SetFilters(None, f, True),
        )
        radio.pack(side="left", padx=(0, 30))

    # 3. Prazo para Exclusão
    time_section_ad = customtkinter.CTkFrame(options_frame_ad, fg_color="transparent")
    time_section_ad.pack(fill="x", padx=20, pady=(15, 20))

    lbl_title_time_ad = customtkinter.CTkLabel(
        time_section_ad,
        text="Prazo para Exclusão",
        font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
        text_color=COLORS["accent_primary"],
    )
    lbl_title_time_ad.pack(anchor="w", pady=(0, 8))

    time_controls_ad = customtkinter.CTkFrame(time_section_ad, fg_color="transparent")
    time_controls_ad.pack(fill="x")

    time_value_ad = autodelete_config.get("AutoDeleteConfig", {}).get(
        "Dias para Auto Deletar", "15"
    )
    valid_times_ad = [
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
    ]
    if str(time_value_ad) not in valid_times_ad:
        DropDownTimeValue_ad = customtkinter.StringVar(value="15")
    else:
        DropDownTimeValue_ad = customtkinter.StringVar(value=str(time_value_ad))

    DropDown_time_ad = customtkinter.CTkOptionMenu(
        time_controls_ad,
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
        variable=DropDownTimeValue_ad,
        command=lambda x: timeVerification.DaysAutoDelete(x).Setdays(),
        values=valid_times_ad,
        dynamic_resizing=False,
        corner_radius=8,
    )
    DropDown_time_ad.pack(side="left")

    description_time_ad = customtkinter.CTkLabel(
        time_controls_ad,
        text="Dias para excluir o arquivo após ser detectado.",
        font=customtkinter.CTkFont(family="Segoe UI", size=12),
        text_color=COLORS["text_secondary"],
    )
    description_time_ad.pack(side="left", padx=(10, 0))

    window.mainloop()


if __name__ == "__main__":
    open_config_window(None)
