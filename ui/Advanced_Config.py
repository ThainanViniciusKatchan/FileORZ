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
from utils.AdvancedConfig import AdvancedConfig
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
}

adv_config = AdvancedConfig()
keywords_data = adv_config.load_keywords()


def open_advanced_config_window(parent):
    t = Translate()
    icon_dir = os.path.join(str(os.path.dirname(__file__)), "icon")
    icon_path = os.path.join(icon_dir, "IconApp.ico")

    window = customtkinter.CTkToplevel(parent)
    if parent:
        window.transient(parent)
    window.title(t.get_text("Adivanced_config", "tittle") or "Configurações Avançadas - FileORZ (BETA)")
    window.geometry("800x650")
    window.configure(fg_color=COLORS["bg_primary"])
    window.resizable(False, False)
    window.grab_set()
    Centralizar_Janela(window, 800, 650)
    window.lift()
    window.focus_force()
    window.after(100, lambda: (window.lift(), window.focus_force()))

    try:
        if os.path.exists(icon_path):
            window.after(200, lambda: window.iconbitmap(icon_path))
    except Warning:
        pass

    # Header
    header_frame = customtkinter.CTkFrame(
        window, fg_color="#1E1E3F", corner_radius=0, height=60
    )
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    header_inner = customtkinter.CTkFrame(header_frame, fg_color="transparent")
    header_inner.pack(fill="both", expand=True, padx=25, pady=12)

    header_icon = customtkinter.CTkLabel(
        header_inner, text="🧠", font=customtkinter.CTkFont(size=22)
    )
    header_icon.pack(side="left")

    header_title = customtkinter.CTkLabel(
        header_inner,
        text=t.get_text("Adivanced_config", "header") or "Organização Avançada de Documentos (BETA)",
        font=customtkinter.CTkFont(family="Segoe UI", size=18, weight="bold"),
        text_color=COLORS["text_primary"],
    )
    header_title.pack(side="left", padx=(10, 0))

    # Control Frame (Ativar + Adicionar)
    control_frame = customtkinter.CTkFrame(window, fg_color="transparent")
    control_frame.pack(fill="x", padx=30, pady=10)

    # Checkbox para ativar/desativar
    advanced_var = customtkinter.BooleanVar(value=adv_config.get_enabled())

    def toggle_advanced():
        tr = Translate()
        adv_config.set_enabled(advanced_var.get())
        if advanced_var.get():
            checkbox.configure(
                text=tr.get_text("Adivanced_config", "mode_adv_enable") or "Modo Avançado Ativado"
            )
        else:
            checkbox.configure(
                text=tr.get_text("Adivanced_config", "mode_adv_disable") or "Modo Avançado Desativado"
            )

    texto_ativado = t.get_text("Adivanced_config", "mode_adv_enable") or "Modo Avançado Ativado"
    texto_desativado = t.get_text("Adivanced_config", "mode_adv_disable") or "Modo Avançado Desativado"
    checkbox_text = (
        texto_ativado if advanced_var.get() else texto_desativado
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

    # Botão Adicionar Grupo
    def add_group():
        # Adiciona um grupo temporário vazio no início se não houver um em edição
        if "" not in keywords_data:
            # Criamos um dicionário novo para colocar o vazio no topo
            new_data = {"": []}
            new_data.update(keywords_data)
            adv_config.save_keywords(new_data)
            refresh_keywords()

    btn_add = customtkinter.CTkButton(
        control_frame,
        text=t.get_text("Adivanced_config", "btn_add") or "+ Adicionar Grupo",
        command=add_group,
        fg_color=COLORS["accent_success"],
        hover_color=COLORS["accent_success_hover"],
        font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
        width=150,
        height=35,
        corner_radius=8,
    )
    btn_add.pack(side="right")

    # Descrição
    description_text = (
        t.get_text("Adivanced_config", "description")
        or "Defina o nome do grupo e as palavras-chave (separadas por vírgula) para organizar seus PDFs.\n"
        "Clique no ícone de salvar em cada card para aplicar as alterações."
    )
    description = customtkinter.CTkLabel(
        window,
        text=description_text,
        font=customtkinter.CTkFont(family="Segoe UI", size=12),
        text_color=COLORS["text_secondary"],
        justify="left",
    )
    description.pack(padx=30, pady=(0, 10), anchor="w")

    # Keywords Container
    keywords_scroll = customtkinter.CTkScrollableFrame(
        window,
        fg_color=COLORS["bg_secondary"],
        border_width=1,
        border_color=COLORS["border"],
        corner_radius=12,
    )
    keywords_scroll.pack(fill="both", expand=True, padx=30, pady=(10, 20))

    def refresh_keywords():
        # Limpa o frame atual
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
            # Card do Grupo
            group_card = customtkinter.CTkFrame(
                keywords_scroll,
                fg_color=COLORS["bg_card"],
                corner_radius=10,
                border_width=1,
                border_color=COLORS["border"],
            )
            group_card.pack(fill="x", padx=10, pady=8)

            # Header do Card (Título Editável + Botão Excluir)
            card_header = customtkinter.CTkFrame(group_card, fg_color="transparent")
            card_header.pack(fill="x", padx=15, pady=(10, 5))

            # Entry para o Nome do Grupo
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
                global keywords_data
                keywords_data = adv_config.load_keywords()
                if cat in keywords_data:
                    del keywords_data[cat]
                    adv_config.save_keywords(keywords_data)
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

            # Input de Palavras-chave
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

                # Se o nome mudou ou era um novo grupo, remove o antigo/temporário
                if old_cat in data:
                    del data[old_cat]

                data[new_cat] = new_words
                adv_config.save_keywords(data)

                # Feedback e Refresh
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

    # Carrega os dados inicialmente
    refresh_keywords()

    if parent is None:
        window.mainloop()


if __name__ == "__main__":
    open_advanced_config_window(None)
