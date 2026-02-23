import customtkinter
import os
import sys
from Centralizar_Janela import Centralizar_Janela

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import load_config, save_config

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

def open_config_window(parent):
    icon_dir = os.path.join(os.path.dirname(__file__), "icon")
    icon_path = os.path.join(icon_dir, "IconApp.ico")
    
    window = customtkinter.CTkToplevel(parent)
    window.title("Configurações - FileORZ")
    window.geometry("900x650")
    window.configure(fg_color=COLORS["bg_primary"])
    window.resizable(False, False)
    window.grab_set()
    Centralizar_Janela(window, 900, 650)
    
    try:
        if os.path.exists(icon_path):
            window.after(200, lambda: window.iconbitmap(icon_path))
    except Exception:
        pass
    
    config = load_config()
    
    extension_vars = {}
    
    header_frame = customtkinter.CTkFrame(window, fg_color="#1E1E3F", corner_radius=0, height=60)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    header_inner = customtkinter.CTkFrame(header_frame, fg_color="transparent")
    header_inner.pack(fill="both", expand=True, padx=25, pady=12)
    
    header_icon = customtkinter.CTkLabel(
        header_inner,
        text="⚙️",
        font=customtkinter.CTkFont(size=22)
    )
    header_icon.pack(side="left")
    
    header_title = customtkinter.CTkLabel(
        header_inner, 
        text="Configurar Extensões por Categoria",
        font=customtkinter.CTkFont(family="Segoe UI", size=18, weight="bold"),
        text_color=COLORS["text_primary"]
    )
    header_title.pack(side="left", padx=(10, 0))
    
    header_subtitle = customtkinter.CTkLabel(
        header_inner,
        text="Selecione quais tipos de arquivo serão organizados",
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color=COLORS["text_secondary"]
    )
    header_subtitle.pack(side="right")
    
    scroll_frame = customtkinter.CTkScrollableFrame(
        window, 
        width=860, 
        height=480,
        fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["accent_primary"],
        scrollbar_button_hover_color=COLORS["accent_hover"]
    )
    scroll_frame.pack(pady=15, padx=15, fill="both", expand=True)
    
    for category, extensions in config.items():
        if category == "Folder" or category == "AutoDelete" or category == "AutoDeleteConfig":
            continue

        if not isinstance(extensions, dict):
            continue
        
        extension_vars[category] = {}
        
        cat_frame = customtkinter.CTkFrame(
            scroll_frame, 
            fg_color=COLORS["bg_secondary"], 
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        cat_frame.pack(pady=8, padx=5, fill="x")
        
        # Cabeçalho da categoria
        header_container = customtkinter.CTkFrame(cat_frame, fg_color="transparent")
        header_container.pack(fill="x", padx=18, pady=(15, 10))
        
        # Lado esquerdo: nome da categoria
        cat_left = customtkinter.CTkFrame(header_container, fg_color="transparent")
        cat_left.pack(side="left")
        
        cat_icon = customtkinter.CTkLabel(
            cat_left,
            text="📁",
            font=customtkinter.CTkFont(size=16)
        )
        cat_icon.pack(side="left")
        
        cat_label = customtkinter.CTkLabel(
            cat_left,
            text=category.upper(),
            font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLORS["text_category"]
        )
        cat_label.pack(side="left", padx=(8, 0))
        
        # Contador de extensões selecionadas
        enabled_count = sum(1 for v in extensions.values() if v)
        total_count = len(extensions)
        count_label = customtkinter.CTkLabel(
            cat_left,
            text=f"  •  {enabled_count}/{total_count} selecionadas",
            font=customtkinter.CTkFont(family="Segoe UI", size=11),
            text_color=COLORS["text_secondary"]
        )
        count_label.pack(side="left")
        
        # Lado direito: botões de ação
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
            corner_radius=6
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
            corner_radius=6
        )
        btn_deselect_all.pack(side="left")
        
        # Grid de Extensões
        ext_frame = customtkinter.CTkFrame(
            cat_frame, 
            fg_color=COLORS["bg_card_inner"], 
            corner_radius=8
        )
        ext_frame.pack(fill="x", padx=18, pady=(5, 18))
        
        # Criar checkboxes para cada extensão em grid
        row = 0
        col = 0
        max_cols = 6
        
        for ext, enabled in extensions.items():
            # Criar variável para a checkbox
            var = customtkinter.BooleanVar(value=enabled)
            extension_vars[category][ext] = var
            
            # Checkbox da extensão
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
                corner_radius=4
            )
            checkbox.grid(row=row, column=col, padx=10, pady=8, sticky="w")
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Padding extra se a última linha não estiver completa
        if col > 0:
            for empty_col in range(col, max_cols):
                spacer = customtkinter.CTkLabel(ext_frame, text="", width=120)
                spacer.grid(row=row, column=empty_col)
    
    # BOTÃO SALVAR
    footer_frame = customtkinter.CTkFrame(window, fg_color=COLORS["bg_secondary"], height=70)
    footer_frame.pack(fill="x", side="bottom")
    footer_frame.pack_propagate(False)
    
    footer_inner = customtkinter.CTkFrame(footer_frame, fg_color="transparent")
    footer_inner.pack(fill="both", expand=True, padx=25, pady=12)
    
    # Label de feedback
    feedback_container = customtkinter.CTkFrame(footer_inner, fg_color="transparent")
    feedback_container.pack(side="left", fill="y")
    
    # Função para salvar as alterações
    def save_changes():
        config = load_config()
        
        for category, exts in extension_vars.items():
            if category in config:
                for ext, var in exts.items():
                    config[category][ext] = var.get()
        
        save_config(config)
        
        # Mostra mensagem de sucesso
        success_label = customtkinter.CTkLabel(
            feedback_container,
            text="✓  Configurações salvas com sucesso!",
            font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=COLORS["accent_success"]
        )
        success_label.pack(side="left", anchor="center")
        window.after(2500, success_label.destroy)
    
    # Botão Salvar
    save_button = customtkinter.CTkButton(
        footer_inner,
        text="💾  Salvar Configurações",
        command=save_changes,
        fg_color=COLORS["accent_primary"],
        hover_color=COLORS["accent_hover"],
        font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
        width=220,
        height=45,
        corner_radius=10
    )
    save_button.pack(side="right")


if __name__ == "__main__":
    open_config_window(None)
