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

import os
import sys
import customtkinter
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import toggle_startup as toggle_startup_registry, script_dir
from utils import StartUp
from utils.translate import Translate
from ui.Centralizar_Janela import Centralizar_Janela

COLORS = {
    "header_gradient_start": "#667eea",
    "header_gradient_end": "#764ba2",
    "header_bg": "#1E1E3F",
    "button_bg": "#2D2D44",
    "button_hover": "#3D3D54",
    "button_border": "#4D4D64",
    "text_primary": "#FFFFFF",
    "accent": "#9D4EDD",
    "accent_hover": "#7B2CBF",
    "switch_progress": "#9D4EDD",
    "switch_bg": "#2D2D44",
    "bg_primary": "#0D0D0D",
    "bg_secondary": "#1A1A2E",
}

def get_language_options():
    try:
        locate_path = os.path.join(script_dir(), "locate")
        if not os.path.exists(locate_path):
            locate_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "locate"
            )
        if os.path.exists(locate_path):
            files = [
                os.path.splitext(f)[0]
                for f in os.listdir(locate_path)
                if f.endswith(".json")
            ]
            if files:
                if "pt-br" not in files:
                    files.append("pt-br")
                return sorted(files)
    except Exception as e:
        print(f"Erro ao listar idiomas: {e}")
    return ["de", "en", "es", "pt-br", "ru", "zh"]

def language_button(parent):
    options = get_language_options()
    translator = Translate()

    try:
        current_lang = translator.get_locate()
        if not current_lang or current_lang not in options:
            current_lang = "pt-br"
            translator.set_locate(lang="pt-br")
    except Exception:
        current_lang = "pt-br"

    lang_var = customtkinter.StringVar(value=current_lang)

    def on_change(selected_lang):
        translator.set_locate(lang=selected_lang)

    dropdown = customtkinter.CTkOptionMenu(
        parent,
        values=options,
        variable=lang_var,
        command=on_change,
        font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
        dropdown_font=customtkinter.CTkFont(family="Segoe UI", size=12),
        fg_color=COLORS["button_bg"],
        button_color=COLORS["accent"],
        button_hover_color=COLORS["accent_hover"],
        text_color=COLORS["text_primary"],
        dropdown_fg_color=COLORS["button_bg"],
        dropdown_text_color=COLORS["text_primary"],
        dropdown_hover_color=COLORS["accent_hover"],
        corner_radius=8,
        height=32,
        width=85,
        dynamic_resizing=False,
    )
    return dropdown

def changelog_button(parent):
    t = Translate()
    btn = customtkinter.CTkButton(
        parent, 
        text=t.get_text("header", "changelog_title") or "Changelog",
        font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
        fg_color=COLORS["button_bg"], 
        border_width=1,
        border_color=COLORS["button_border"],
        corner_radius=8,
        height=32,
        width=90,
        hover_color=COLORS["button_hover"],
        text_color=COLORS["text_primary"]
    )
    btn.bind("<Button-1>", lambda event:
    webbrowser.open("https://thainanviniciuskatchan.github.io/FileORZ/changelog.html"))
    return btn

def git_button(parent):
    t = Translate()
    btn = customtkinter.CTkButton(
        parent, 
        text=t.get_text("header", "github_title") or "GitHub",
        font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
        fg_color=COLORS["button_bg"], 
        border_width=1,
        border_color=COLORS["button_border"],
        corner_radius=8,
        height=32,
        width=90,
        hover_color=COLORS["button_hover"],
        text_color=COLORS["text_primary"]
    )
    btn.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/ThainanViniciusKatchan/FileORZ"))
    return btn

def open_about_window(parent=None):
    t = Translate()
    icon_dir = os.path.join(os.path.dirname(__file__), "icon")
    icon_path = os.path.join(icon_dir, "IconApp.ico")

    window = customtkinter.CTkToplevel(parent)
    if parent:
        window.transient(parent)
    window.title(t.get_text("header", "about_title") or "Sobre - FileORZ")
    window.geometry("420x260")
    window.configure(fg_color=COLORS["bg_primary"])
    window.resizable(False, False)
    window.grab_set()
    Centralizar_Janela(window, 420, 260)
    window.lift()
    window.focus_force()
    window.after(100, lambda: (window.lift(), window.focus_force()))

    try:
        if os.path.exists(icon_path):
            window.after(200, lambda: window.iconbitmap(icon_path))
    except Exception:
        pass

    # Header da janela Sobre
    header_frame = customtkinter.CTkFrame(
        window, fg_color=COLORS["header_bg"], corner_radius=0, height=55
    )
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)

    header_inner = customtkinter.CTkFrame(header_frame, fg_color="transparent")
    header_inner.pack(fill="both", expand=True, padx=20, pady=10)

    header_icon = customtkinter.CTkLabel(
        header_inner, text="🗂️", font=customtkinter.CTkFont(size=20)
    )
    header_icon.pack(side="left", padx=(0, 6))

    header_title = customtkinter.CTkLabel(
        header_inner,
        text="FileORZ",
        font=customtkinter.CTkFont(family="Segoe UI", size=18, weight="bold"),
        text_color=COLORS["text_primary"],
    )
    header_title.pack(side="left")

    header_subtitle = customtkinter.CTkLabel(
        header_inner,
        text=t.get_text("header", "subtitle") or "Organizador de Arquivos",
        font=customtkinter.CTkFont(family="Segoe UI", size=10),
        text_color="#A0A0A0",
    )
    header_subtitle.pack(side="left", padx=(8, 0))

    # Container de conteúdo
    content_frame = customtkinter.CTkFrame(
        window,
        fg_color=COLORS["bg_secondary"],
        corner_radius=12,
        border_width=1,
        border_color=COLORS["button_border"],
    )
    content_frame.pack(fill="both", expand=True, padx=20, pady=15)

    # Frame para os botões Changelog e GitHub
    buttons_frame = customtkinter.CTkFrame(content_frame, fg_color="transparent")
    buttons_frame.pack(pady=(16, 12))

    changelog = changelog_button(buttons_frame)
    changelog.pack(side="left", padx=(0, 10))

    git = git_button(buttons_frame)
    git.pack(side="left")

    # Frase "Desenvolvido com orgulho no Brasil 💚💛"
    pride_label = customtkinter.CTkLabel(
        content_frame,
        text=t.get_text("header", "about_pride") or "Desenvolvido com orgulho no Brasil 💚💛",
        font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
        text_color=COLORS["text_primary"],
    )
    pride_label.pack(pady=(2, 2))

    # "Desenvolvido por: Thainan Vinicius Katchan"
    author_label = customtkinter.CTkLabel(
        content_frame,
        text=t.get_text("header", "about_dev_by") or "Desenvolvido por: Thainan Vinicius Katchan",
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color="#A0A0A0",
    )
    author_label.pack(pady=(0, 10))

    def update_about_texts():
        tr = Translate()
        if not window.winfo_exists():
            return
        window.title(tr.get_text("header", "about_title") or "Sobre - FileORZ")
        header_subtitle.configure(
            text=tr.get_text("header", "subtitle") or "Organizador de Arquivos"
        )
        git.configure(text=tr.get_text("header", "github_title") or "GitHub")
        changelog.configure(
            text=tr.get_text("header", "changelog_title") or "Changelog"
        )
        pride_label.configure(
            text=tr.get_text("header", "about_pride") or "Desenvolvido com orgulho no Brasil 💚💛"
        )
        author_label.configure(
            text=tr.get_text("header", "about_dev_by") or "Desenvolvido por: Thainan Vinicius Katchan"
        )

    Translate.register_listener(update_about_texts)

    def on_close():
        Translate.unregister_listener(update_about_texts)
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

    if parent is None:
        window.mainloop()

def about_button(parent, root=None):
    t = Translate()
    btn = customtkinter.CTkButton(
        parent,
        text=t.get_text("header", "about_btn") or "Sobre",
        font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
        fg_color=COLORS["button_bg"],
        border_width=1,
        border_color=COLORS["button_border"],
        corner_radius=8,
        height=32,
        width=80,
        hover_color=COLORS["button_hover"],
        text_color=COLORS["text_primary"],
        command=lambda: open_about_window(root or parent),
    )
    return btn

# Essa Função Controla a Inicialização da Aplicação no Windows, Alterando o Json de Configuração
# e Criando o Registro de StartUp
def startup_button(parent):
    Start = StartUp.StartUpSys()
    startup_var = customtkinter.BooleanVar(value=Start.GetEnabled)
    config_obj = StartUp.StartUpSys()
    t = Translate()
    print(f"config StartUp: {config_obj.GetEnabled}")

    def toggle_startup():
        new_value = startup_var.get()
        print(f"Novo valor: {new_value}")
        config_obj.enabled = new_value
        toggle_startup_registry(new_value)

    startup_switch = customtkinter.CTkSwitch(
        parent,
        text=t.get_text("header", "startup") or "Iniciar com Windows",
        command=toggle_startup,
        variable=startup_var,
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color=COLORS["text_primary"],
        fg_color=COLORS["switch_bg"],
        progress_color=COLORS["switch_progress"],
        button_color=COLORS["text_primary"],
        button_hover_color="#E0E0E0"
    )
    startup_switch.pack(side="left", padx=(0, 15))
    return startup_switch

# Função Principal que cria o header na aplicação
def header(root):
    t = Translate()
    header_frame = customtkinter.CTkFrame(
        root,
        fg_color=COLORS["header_bg"],
        corner_radius=0,
        height=60
    )
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)

    inner_container = customtkinter.CTkFrame(header_frame, fg_color="transparent")
    inner_container.pack(fill="both", expand=True, padx=20, pady=10)

    logo_frame = customtkinter.CTkFrame(inner_container, fg_color="transparent")
    logo_frame.pack(side="left", anchor="center")

    icon_label = customtkinter.CTkLabel(
        logo_frame,
        text="🗂️",
        font=customtkinter.CTkFont(size=24)
    )
    icon_label.pack(side="left", padx=(0, 5))

    # Nome da aplicação
    title_label = customtkinter.CTkLabel(
        logo_frame,
        text="FileORZ",
        font=customtkinter.CTkFont(family="Segoe UI", size=22, weight="bold"),
        text_color=COLORS["text_primary"]
    )
    title_label.pack(side="left")

    # Subtítulo
    subtitle_label = customtkinter.CTkLabel(
        logo_frame,
        text=t.get_text("header", "subtitle") or "Organizador de Arquivos",
        font=customtkinter.CTkFont(family="Segoe UI", size=10),
        text_color="#A0A0A0"
    )
    subtitle_label.pack(side="left", padx=(10, 0))

    controls_frame = customtkinter.CTkFrame(inner_container, fg_color="transparent")
    controls_frame.pack(side="right", anchor="center")

    switch_widget = startup_button(controls_frame)

    # Botão de Idioma
    lang_btn = language_button(controls_frame)
    lang_btn.pack(side="left", padx=(0, 12))

    # Botão Sobre
    about_btn = about_button(controls_frame, root)
    about_btn.pack(side="left")

    def update_header_texts():
        tr = Translate()
        subtitle_label.configure(text=tr.get_text("header", "subtitle") or "Organizador de Arquivos")
        switch_widget.configure(text=tr.get_text("header", "startup") or "Iniciar com Windows")
        about_btn.configure(text=tr.get_text("header", "about_btn") or "Sobre")

    Translate.register_listener(update_header_texts)

    return header_frame


if __name__ == "__main__":
    root = customtkinter.CTk()
    root.geometry("700x50")
    root.title("FileORZ")
    root.configure(bg=COLORS["header_bg"])
    header(root)
    root.mainloop()