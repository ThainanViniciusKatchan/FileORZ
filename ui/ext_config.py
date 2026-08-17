import os
import sys
import customtkinter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ui.Centralizar_Janela import Centralizar_Janela
except ImportError:
    from Centralizar_Janela import Centralizar_Janela

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


def ext_config_window(parent=None):
    t = Translate()
    icon_dir = os.path.join(os.path.dirname(__file__), "icon")
    icon_path = os.path.join(icon_dir, "IconApp.ico")

    window = customtkinter.CTkToplevel(parent)
    if parent:
        window.transient(parent)
    window.title(t.get_text("ext_config", "tittle_ext_config") or "Categorias e Extensões - FileORZ")
    window.geometry("900x700")
    window.configure(fg_color=COLORS["bg_primary"])
    window.resizable(False, False)
    window.grab_set()
    Centralizar_Janela(window, 900, 700)
    window.lift()
    window.focus_force()
    window.after(100, lambda: (window.lift(), window.focus_force()))

    try:
        if os.path.exists(icon_path):
            window.after(200, lambda: window.iconbitmap(icon_path))
    except Exception:
        pass

    # Header da Janela
    header_frame = customtkinter.CTkFrame(
        window, fg_color="#1E1E3F", corner_radius=0, height=65
    )
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)

    header_inner = customtkinter.CTkFrame(header_frame, fg_color="transparent")
    header_inner.pack(fill="both", expand=True, padx=25, pady=12)

    header_icon = customtkinter.CTkLabel(
        header_inner, text="📁", font=customtkinter.CTkFont(size=22)
    )
    header_icon.pack(side="left")

    header_title = customtkinter.CTkLabel(
        header_inner,
        text=t.get_text("ext_config", "header") or "Categorias e Extensões",
        font=customtkinter.CTkFont(family="Segoe UI", size=18, weight="bold"),
        text_color=COLORS["text_primary"],
    )
    header_title.pack(side="left", padx=(10, 0))

    header_subtitle = customtkinter.CTkLabel(
        header_inner,
        text=t.get_text("ext_config", "header_subtitle") or "Gerencie as extensões por categoria",
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color=COLORS["text_secondary"],
    )
    header_subtitle.pack(side="right")

    # Footer (com botão de salvar e feedback)
    footer_frame = customtkinter.CTkFrame(
        window, fg_color=COLORS["bg_secondary"], height=60, corner_radius=10
    )
    footer_frame.pack(fill="x", side="bottom", padx=15, pady=(5, 15))
    footer_frame.pack_propagate(False)

    footer_inner = customtkinter.CTkFrame(footer_frame, fg_color="transparent")
    footer_inner.pack(fill="both", expand=True, padx=15, pady=10)

    feedback_container = customtkinter.CTkFrame(footer_inner, fg_color="transparent")
    feedback_container.pack(side="left", fill="y")

    # Frame rolável central
    scroll_frame = customtkinter.CTkScrollableFrame(
        window,
        width=840,
        fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["accent_primary"],
        scrollbar_button_hover_color=COLORS["accent_hover"],
    )
    scroll_frame.pack(pady=10, padx=15, fill="both", expand=True)

    config = load_config("dist", "category")
    extension_vars = {}

    for category, extensions in config.items():
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
            text=t.get_text("ext_config", "btn_select_all") or "✓ Todos",
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
            text=t.get_text("ext_config", "btn_deselect_all") or "✗ Nenhum",
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

    def save_changes():
        config_data = load_config("dist", "category")

        for category, exts in extension_vars.items():
            if category in config_data:
                for ext, var in exts.items():
                    config_data[category][ext] = var.get()

        save_config("dist", "category", config_data)

        for widget in feedback_container.winfo_children():
            widget.destroy()

        success_msg = Translate().get_text("ext_config", "success_label") or "✓  Configurações salvas com sucesso!"
        success_label = customtkinter.CTkLabel(
            feedback_container,
            text=success_msg,
            font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=COLORS["accent_success"],
        )
        success_label.pack(side="left", anchor="center")
        window.after(2500, success_label.destroy)

    save_button = customtkinter.CTkButton(
        footer_inner,
        text=t.get_text("ext_config", "btn_save") or "💾  Salvar Categorias",
        command=save_changes,
        fg_color=COLORS["accent_primary"],
        hover_color=COLORS["accent_hover"],
        font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
        width=200,
        height=40,
        corner_radius=8,
    )
    save_button.pack(side="right")

    def update_ext_config_texts():
        tr = Translate()
        if not window.winfo_exists():
            return
        window.title(tr.get_text("ext_config", "tittle_ext_config") or "Categorias e Extensões - FileORZ")
        header_title.configure(text=tr.get_text("ext_config", "header") or "Categorias e Extensões")
        header_subtitle.configure(text=tr.get_text("ext_config", "header_subtitle") or "Gerencie as extensões por categoria")
        save_button.configure(text=tr.get_text("ext_config", "btn_save") or "💾  Salvar Categorias")

    Translate.register_listener(update_ext_config_texts)

    def on_close():
        Translate.unregister_listener(update_ext_config_texts)
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

    if parent is None:
        window.mainloop()


open_ext_config_window = ext_config_window

if __name__ == "__main__":
    ext_config_window(None)
