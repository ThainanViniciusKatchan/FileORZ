import customtkinter
import webbrowser
import os 
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import get_startup, set_startup, is_startup_enabled, toggle_startup as toggle_startup_registry

# ═══════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM - Cores Premium
# ═══════════════════════════════════════════════════════════════════════════════
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
}

def header(root):
    """Cria o header moderno com gradiente e controles estilizados"""
    
    # Frame principal do header com cor sólida elegante
    header_frame = customtkinter.CTkFrame(
        root, 
        fg_color=COLORS["header_bg"], 
        corner_radius=0, 
        height=60
    )
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)  # Mantém altura fixa
    
    # Container interno para padding
    inner_container = customtkinter.CTkFrame(header_frame, fg_color="transparent")
    inner_container.pack(fill="both", expand=True, padx=20, pady=10)
    
    # ── Logo e Título ──────────────────────────────────────────────────────────
    logo_frame = customtkinter.CTkFrame(inner_container, fg_color="transparent")
    logo_frame.pack(side="left", anchor="center")
    
    # Ícone decorativo
    icon_label = customtkinter.CTkLabel(
        logo_frame,
        text="🗂️",
        font=customtkinter.CTkFont(size=24)
    )
    icon_label.pack(side="left", padx=(0, 8))
    
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
        text="Organizador de Arquivos",
        font=customtkinter.CTkFont(family="Segoe UI", size=10),
        text_color="#A0A0A0"
    )
    subtitle_label.pack(side="left", padx=(10, 0))
    
    # ── Controles do lado direito ──────────────────────────────────────────────
    controls_frame = customtkinter.CTkFrame(inner_container, fg_color="transparent")
    controls_frame.pack(side="right", anchor="center")
    
    # Switch de iniciar com Windows
    startup_switch = startup_button(controls_frame)
    startup_switch.pack(side="left", padx=(0, 15))
    
    # Botão GitHub
    git = git_button(controls_frame)
    git.pack(side="left")
    
    return header_frame

def git_button(parent):
    """Botão do GitHub com estilo glass moderno"""
    btn = customtkinter.CTkButton(
        parent, 
        text="GitHub",
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


def startup_button(parent):
    """Switch de startup com estilo moderno"""
    
    startup_var = customtkinter.BooleanVar(value=get_startup())

    def on_toggle():
        is_enabled = startup_var.get()
        # Atualiza o config.json
        set_startup(is_enabled)
        # Cria ou remove o registro do Windows
        toggle_startup_registry(is_enabled)

    startup_switch = customtkinter.CTkSwitch(
        parent, 
        text="Iniciar com Windows",
        command=on_toggle,
        variable=startup_var,
        font=customtkinter.CTkFont(family="Segoe UI", size=11),
        text_color=COLORS["text_primary"],
        fg_color=COLORS["switch_bg"],
        progress_color=COLORS["switch_progress"],
        button_color=COLORS["text_primary"],
        button_hover_color="#E0E0E0"
    )

    return startup_switch