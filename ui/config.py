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
from utils.AdvancedConfig import AdvancedConfig
from utils.translate import Translate
from ui.Centralizar_Janela import Centralizar_Janela
from ui.ext_config import ext_config_window
from ui.Advanced_Config import open_advanced_config_window
from ui.Config_AutoDell import open_Windows_CFG_autoDell

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
    t = Translate()
    icon_dir = os.path.join(os.path.dirname(__file__), "icon")
    icon_path = os.path.join(icon_dir, "IconApp.ico")

    window = customtkinter.CTkToplevel(parent)
    if parent:
        window.transient(parent)
    window.title(t.get_text("Config_Window", "tittle_ext_config") or "Configurações Gerais - FileORZ")
    window.geometry("900x520")
    window.configure(fg_color=COLORS["bg_primary"])
    window.resizable(False, False)
    window.grab_set()
    Centralizar_Janela(window, 900, 520)
    window.lift()
    window.focus_force()
    window.after(100, lambda: (window.lift(), window.focus_force()))

    try:
        if os.path.exists(icon_path):
            window.after(200, lambda: window.iconbitmap(icon_path))
    except Exception:
        pass

    header_frame = customtkinter.CTkFrame(
        window, fg_color="#1E1E3F", corner_radius=0, height=65
    )
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)

    header_inner = customtkinter.CTkFrame(header_frame, fg_color="transparent")
    header_inner.pack(fill="both", expand=True, padx=25, pady=12)

    header_icon = customtkinter.CTkLabel(
        header_inner, text="⚙️", font=customtkinter.CTkFont(size=22)
    )
    header_icon.pack(side="left")

    header_title = customtkinter.CTkLabel(
        header_inner,
        text=t.get_text("Config_Window", "header") or "Configuração - FileORZ",
        font=customtkinter.CTkFont(family="Segoe UI", size=18, weight="bold"),
        text_color=COLORS["text_primary"],
    )
    header_title.pack(side="left", padx=(10, 0))

    header_subtitle = customtkinter.CTkLabel(
        header_inner,
        text=t.get_text("Config_Window", "header_subtitle") or "Ajuste as preferências do organizador",
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color=COLORS["text_secondary"],
    )
    header_subtitle.pack(side="right")

    cards_container = customtkinter.CTkFrame(window, fg_color="transparent")
    cards_container.place(relx=0.5, rely=0.56, anchor="center")

    card_ext = customtkinter.CTkFrame(
        cards_container,
        fg_color=COLORS["bg_secondary"],
        corner_radius=14,
        border_width=1,
        border_color=COLORS["border"],
        width=250,
        height=360,
    )
    card_ext.pack(side="left", padx=12)
    card_ext.pack_propagate(False)

    lbl_ext_icon = customtkinter.CTkLabel(
        card_ext, text="📁", font=customtkinter.CTkFont(size=44)
    )
    lbl_ext_icon.pack(pady=(35, 10))

    lbl_ext_title = customtkinter.CTkLabel(
        card_ext,
        text=t.get_text("Config_Window", "lbl_ext_title") or "Categorias &\nExtensões",
        font=customtkinter.CTkFont(family="Segoe UI", size=16, weight="bold"),
        text_color=COLORS["text_primary"],
        justify="center",
    )
    lbl_ext_title.pack(pady=(0, 10))

    lbl_ext_desc = customtkinter.CTkLabel(
        card_ext,
        text=t.get_text("Config_Window", "lbl_ext_desc") or "Gerencie e customize as extensões de arquivos organizadas por categoria.",
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color=COLORS["text_secondary"],
        justify="center",
        wraplength=210,
    )
    lbl_ext_desc.pack(pady=(0, 25))

    btn_ext = customtkinter.CTkButton(
        card_ext,
        text=t.get_text("Config_Window", "btn_config") or "⚙️ Configurar",
        command=lambda: ext_config_window(window),
        fg_color=COLORS["accent_primary"],
        hover_color=COLORS["accent_hover"],
        font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
        width=190,
        height=40,
        corner_radius=8,
    )
    btn_ext.pack(side="bottom", pady=30)

    card_adv = customtkinter.CTkFrame(
        cards_container,
        fg_color=COLORS["bg_secondary"],
        corner_radius=14,
        border_width=1,
        border_color=COLORS["border"],
        width=250,
        height=360,
    )
    card_adv.pack(side="left", padx=12)
    card_adv.pack_propagate(False)

    lbl_adv_icon = customtkinter.CTkLabel(
        card_adv, text="🧠", font=customtkinter.CTkFont(size=44)
    )
    lbl_adv_icon.pack(pady=(35, 10))

    lbl_adv_title = customtkinter.CTkLabel(
        card_adv,
        text=t.get_text("Config_Window", "lbl_adv_title") or "Organização\nAvançada (BETA)",
        font=customtkinter.CTkFont(family="Segoe UI", size=16, weight="bold"),
        text_color=COLORS["text_primary"],
        justify="center",
    )
    lbl_adv_title.pack(pady=(0, 10))

    lbl_adv_desc = customtkinter.CTkLabel(
        card_adv,
        text=t.get_text("Config_Window", "lbl_adv_desc") or "Regras inteligentes com palavras-chave para agrupar e organizar PDFs.",
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color=COLORS["text_secondary"],
        justify="center",
        wraplength=210,
    )
    lbl_adv_desc.pack(pady=(0, 25))

    btn_adv = customtkinter.CTkButton(
        card_adv,
        text=t.get_text("Config_Window", "btn_config") or "⚙️ Configurar",
        command=lambda: open_advanced_config_window(window),
        fg_color=COLORS["accent_primary"],
        hover_color=COLORS["accent_hover"],
        font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
        width=190,
        height=40,
        corner_radius=8,
    )
    btn_adv.pack(side="bottom", pady=30)

    card_auto = customtkinter.CTkFrame(
        cards_container,
        fg_color=COLORS["bg_secondary"],
        corner_radius=14,
        border_width=1,
        border_color=COLORS["border"],
        width=250,
        height=360,
    )
    card_auto.pack(side="left", padx=12)
    card_auto.pack_propagate(False)

    lbl_auto_icon = customtkinter.CTkLabel(
        card_auto, text="🚮", font=customtkinter.CTkFont(size=44)
    )
    lbl_auto_icon.pack(pady=(35, 10))

    lbl_auto_title = customtkinter.CTkLabel(
        card_auto,
        text=t.get_text("Config_Window", "lbl_auto_title") or "Auto\nDeletar",
        font=customtkinter.CTkFont(family="Segoe UI", size=16, weight="bold"),
        text_color=COLORS["text_primary"],
        justify="center",
    )
    lbl_auto_title.pack(pady=(0, 10))

    lbl_auto_desc = customtkinter.CTkLabel(
        card_auto,
        text=t.get_text("Config_Window", "lbl_auto_desc") or "Defina intervalos e regras automáticas de exclusão para limpeza periódica.",
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color=COLORS["text_secondary"],
        justify="center",
        wraplength=210,
    )
    lbl_auto_desc.pack(pady=(0, 25))

    btn_auto = customtkinter.CTkButton(
        card_auto,
        text=t.get_text("Config_Window", "btn_config") or "⚙️ Configurar",
        command=lambda: open_Windows_CFG_autoDell(window),
        fg_color=COLORS["accent_primary"],
        hover_color=COLORS["accent_hover"],
        font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
        width=190,
        height=40,
        corner_radius=8,
    )
    btn_auto.pack(side="bottom", pady=30)

    def update_config_window_texts():
        tr = Translate()
        if not window.winfo_exists():
            return
        window.title(tr.get_text("Config_Window", "tittle_ext_config") or "Configurações Gerais - FileORZ")
        header_title.configure(text=tr.get_text("Config_Window", "header") or "Configuração - FileORZ")
        header_subtitle.configure(text=tr.get_text("Config_Window", "header_subtitle") or "Ajuste as preferências do organizador")
        lbl_ext_title.configure(text=tr.get_text("Config_Window", "lbl_ext_title") or "Categorias &\nExtensões")
        lbl_ext_desc.configure(text=tr.get_text("Config_Window", "lbl_ext_desc") or "Gerencie e customize as extensões de arquivos organizadas por categoria.")
        btn_ext.configure(text=tr.get_text("Config_Window", "btn_config") or "⚙️ Configurar")
        lbl_adv_title.configure(text=tr.get_text("Config_Window", "lbl_adv_title") or "Organização\nAvançada (BETA)")
        lbl_adv_desc.configure(text=tr.get_text("Config_Window", "lbl_adv_desc") or "Regras inteligentes com palavras-chave para agrupar e organizar PDFs.")
        btn_adv.configure(text=tr.get_text("Config_Window", "btn_config") or "⚙️ Configurar")
        lbl_auto_title.configure(text=tr.get_text("Config_Window", "lbl_auto_title") or "Auto\nDeletar")
        lbl_auto_desc.configure(text=tr.get_text("Config_Window", "lbl_auto_desc") or "Defina intervalos e regras automáticas de exclusão para limpeza periódica.")
        btn_auto.configure(text=tr.get_text("Config_Window", "btn_config") or "⚙️ Configurar")

    Translate.register_listener(update_config_window_texts)

    def on_close():
        Translate.unregister_listener(update_config_window_texts)
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

    if parent is None:
        window.mainloop()


if __name__ == "__main__":
    open_config_window(None)
