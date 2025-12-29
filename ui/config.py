import customtkinter
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import load_config, save_config

def open_config_window(parent):
    """Abre a janela de configurações como toplevel da janela principal"""
    
    # Criar janela toplevel e registrar como secundária
    window = customtkinter.CTkToplevel(parent)
    window.title("Configurações")
    window.geometry("800x600")
    window.configure(fg_color="#0f172a") # Slate 900
    window.resizable(False, False)
    
    # É importante garantir que a janela fique no topo
    window.transient(parent) 
    window.grab_set() 
    
    # Carregar configuração atual
    config = load_config()
    
    # Dicionário para armazenar as variáveis das checkboxes de extensão
    extension_vars = {}
    
    # --- HEADER ---
    header_frame = customtkinter.CTkFrame(window, fg_color="#1e293b", height=60, corner_radius=0)
    header_frame.pack(fill="x", side="top")
    
    title_label = customtkinter.CTkLabel(
        header_frame, 
        text="Gerenciar Extensões",
        font=customtkinter.CTkFont(family="Roboto", size=18, weight="bold"),
        text_color="#f1f5f9"
    )
    title_label.pack(pady=15)
    
    # --- FOOTER (Criado antes do conteúdo para garantir espaço) ---
    # Área de Ação (Footer Fixo)
    footer_frame = customtkinter.CTkFrame(window, fg_color="#0f172a", height=80, corner_radius=0)
    footer_frame.pack(fill="x", side="bottom")
    
    # Linha separadora do footer (Pack por último no bottom para ficar "em cima" do footer)
    sep = customtkinter.CTkFrame(window, height=1, fg_color="#334155")
    sep.pack(fill="x", side="bottom", pady=0)
    
    # --- CONTEÚDO (Scroll) ---
    # Frame com scroll para as categorias
    scroll_frame = customtkinter.CTkScrollableFrame(
        window, 
        width=760, 
        height=450,
        fg_color="transparent" # Transparente para usar o fundo da janela
    )
    scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Criar seção para cada categoria (exceto "Folder")
    for category, extensions in config.items():
        if category == "Folder" or category == "timeverification":
            continue
        
        if not isinstance(extensions, dict):
            continue
        
        # Inicializar dicionário para esta categoria
        extension_vars[category] = {}
        
        # Frame da categoria (Card visual)
        cat_frame = customtkinter.CTkFrame(
            scroll_frame, 
            fg_color="#1e293b", # Slate 800 
            corner_radius=12,
            border_width=1,
            border_color="#334155" # Slate 700
        )
        cat_frame.pack(pady=10, padx=5, fill="x")
        
        # Cabeçalho interno da categoria
        header_inner = customtkinter.CTkFrame(cat_frame, fg_color="transparent")
        header_inner.pack(fill="x", padx=20, pady=(15, 10))
        
        # Nome da categoria
        bg_icon = customtkinter.CTkLabel(
            header_inner, 
            text="📁", 
            font=customtkinter.CTkFont(size=20)
        )
        bg_icon.pack(side="left", padx=(0, 10))
        
        cat_label = customtkinter.CTkLabel(
            header_inner,
            text=category.upper(),
            font=customtkinter.CTkFont(family="Roboto", size=14, weight="bold"),
            text_color="#3b82f6" # Blue
        )
        cat_label.pack(side="left")
        
        # Contador
        enabled_count = sum(1 for v in extensions.values() if v == True)
        total_count = len(extensions.values())
        count_label = customtkinter.CTkLabel(
            header_inner,
            text=f"{enabled_count} de {total_count} ativos",
            font=customtkinter.CTkFont(family="Roboto", size=11),
            text_color="#94a3b8" # Slate 400
        )
        count_label.pack(side="right")
        
        # Barra separadora
        separator = customtkinter.CTkFrame(cat_frame, height=2, fg_color="#334155")
        separator.pack(fill="x", padx=20, pady=(0, 15))
        
        # Frame para os botões de controle
        control_frame = customtkinter.CTkFrame(cat_frame, fg_color="transparent")
        control_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        def select_all(cat=category):
            for ext_var in extension_vars[cat].values():
                ext_var.set(True)
        
        def deselect_all(cat=category):
            for ext_var in extension_vars[cat].values():
                ext_var.set(False)
        
        btn_sel_all = customtkinter.CTkButton(
            control_frame, text="Marcar Tudo", command=select_all,
            font=customtkinter.CTkFont(size=10), height=24, width=80,
            fg_color="#334155", hover_color="#475569"
        )
        btn_sel_all.pack(side="left", padx=(0, 10))
        
        btn_desel_all = customtkinter.CTkButton(
            control_frame, text="Desmarcar Tudo", command=deselect_all,
            font=customtkinter.CTkFont(size=10), height=24, width=100,
            fg_color="#334155", hover_color="#475569"
        )
        btn_desel_all.pack(side="left")
        
        # Frame GRID para as extensões
        ext_frame = customtkinter.CTkFrame(cat_frame, fg_color="transparent")
        ext_frame.pack(fill="x", padx=20, pady=(5, 20))
        
        row = 0
        col = 0
        max_cols = 4  # Menos colunas para mais espaço
        
        for ext, enabled in extensions.items():
            var = customtkinter.BooleanVar(value=enabled)
            extension_vars[category][ext] = var
            
            checkbox = customtkinter.CTkCheckBox(
                ext_frame,
                text=ext,
                variable=var,
                font=customtkinter.CTkFont(family="Roboto", size=12),
                fg_color="#3b82f6",
                hover_color="#2563eb",
                border_color="#94a3b8",
                text_color="#e2e8f0",
                width=100
            )
            checkbox.grid(row=row, column=col, padx=10, pady=8, sticky="w")
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    # --- FUNÇÕES DO FOOTER ---
    
    def save_changes():
        config = load_config()
        
        for category, exts in extension_vars.items():
            if category in config:
                for ext, var in exts.items():
                    config[category][ext] = var.get()
        
        save_config(config)
        
        # Feedback visual no botão
        original_text = save_button.cget("text")
        save_button.configure(text="✓ Salvo!", fg_color="#10b981", hover_color="#059669")
        window.after(1500, lambda: save_button.configure(text=original_text, fg_color="#3b82f6", hover_color="#2563eb"))

    # Botão Salvar (Adicionado ao footer frame existente)
    save_button = customtkinter.CTkButton(
        footer_frame,
        text="Salvar Alterações",
        command=save_changes,
        fg_color="#3b82f6",
        hover_color="#2563eb",
        font=customtkinter.CTkFont(family="Roboto", size=14, weight="bold"),
        height=45,
        width=200,
        corner_radius=8
    )
    save_button.pack(pady=20)
