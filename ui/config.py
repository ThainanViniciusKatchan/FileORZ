import customtkinter
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import load_config, save_config

def open_config_window(parent):
    """Abre a janela de configurações como toplevel da janela principal"""
    
    # Criar janela toplevel
    window = customtkinter.CTkToplevel(parent)
    window.title("Configurações")
    window.geometry("800x600")
    window.configure(fg_color="#121212")
    window.resizable(False, False)
    window.grab_set()  # Modal - bloqueia interação com janela principal
    
    # Carregar configuração atual
    config = load_config()
    
    # Dicionário para armazenar as variáveis das checkboxes de extensão
    extension_vars = {}
    
    # Frame com scroll para as categorias
    scroll_frame = customtkinter.CTkScrollableFrame(
        window, 
        width=760, 
        height=480,
        fg_color="#1a1a1a"
    )
    scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Título principal
    title_label = customtkinter.CTkLabel(
        scroll_frame, 
        text="Configurar Extensões por Categoria",
        font=("Montserrat", 18, "bold"),
        text_color="white"
    )
    title_label.pack(pady=(10, 20))
    
    # Criar seção para cada categoria (exceto "Folder")
    for category, extensions in config.items():
        if category == "Folder":
            continue  # Pular a pasta, não é categoria
        
        if not isinstance(extensions, dict):
            continue
        
        # Inicializar dicionário para esta categoria
        extension_vars[category] = {}
        
        # Frame da categoria
        cat_frame = customtkinter.CTkFrame(scroll_frame, fg_color="#252525", corner_radius=10)
        cat_frame.pack(pady=8, padx=10, fill="x")
        
        # Cabeçalho da categoria
        header_frame = customtkinter.CTkFrame(cat_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        # Nome da categoria
        cat_label = customtkinter.CTkLabel(
            header_frame,
            text=f"📁 {category.upper()}",
            font=("Montserrat", 14, "bold"),
            text_color="#4a9eff"
        )
        cat_label.pack(side="left")
        
        # Contador de extensões selecionadas
        enabled_count = sum(1 for v in extensions.values() if v)
        total_count = len(extensions)
        count_label = customtkinter.CTkLabel(
            header_frame,
            text=f"({enabled_count}/{total_count} selecionadas)",
            font=("Montserrat", 10),
            text_color="#888888"
        )
        count_label.pack(side="right")
        
        # Botões "Selecionar Todos" e "Desmarcar Todos"
        btn_frame = customtkinter.CTkFrame(cat_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=5)
        
        def select_all(cat=category):
            for ext_var in extension_vars[cat].values():
                ext_var.set(True)
        
        def deselect_all(cat=category):
            for ext_var in extension_vars[cat].values():
                ext_var.set(False)
        
        btn_select_all = customtkinter.CTkButton(
            btn_frame,
            text="Selecionar Todos",
            command=select_all,
            fg_color="#2d5a2d",
            hover_color="#3d7a3d",
            font=("Montserrat", 9),
            width=100,
            height=25,
            corner_radius=5
        )
        btn_select_all.pack(side="left", padx=(0, 5))
        
        btn_deselect_all = customtkinter.CTkButton(
            btn_frame,
            text="Desmarcar Todos",
            command=deselect_all,
            fg_color="#5a2d2d",
            hover_color="#7a3d3d",
            font=("Montserrat", 9),
            width=100,
            height=25,
            corner_radius=5
        )
        btn_deselect_all.pack(side="left")
        
        # Frame para as extensões (grid)
        ext_frame = customtkinter.CTkFrame(cat_frame, fg_color="#1e1e1e", corner_radius=8)
        ext_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Criar checkboxes para cada extensão em grid
        row = 0
        col = 0
        max_cols = 5  # 5 colunas de extensões
        
        for ext, enabled in extensions.items():
            # Criar variável para a checkbox
            var = customtkinter.BooleanVar(value=enabled)
            extension_vars[category][ext] = var
            
            # Checkbox da extensão
            checkbox = customtkinter.CTkCheckBox(
                ext_frame,
                text=ext,
                variable=var,
                font=("Consolas", 11),
                fg_color="#4a9eff",
                hover_color="#3a8eef",
                border_color="#4a9eff",
                text_color="white",
                width=120
            )
            checkbox.grid(row=row, column=col, padx=8, pady=5, sticky="w")
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Padding extra se a última linha não estiver completa
        if col > 0:
            for empty_col in range(col, max_cols):
                spacer = customtkinter.CTkLabel(ext_frame, text="", width=120)
                spacer.grid(row=row, column=empty_col)
    
    # Função para salvar alterações
    def save_changes():
        config = load_config()
        
        for category, exts in extension_vars.items():
            if category in config:
                for ext, var in exts.items():
                    config[category][ext] = var.get()
        
        save_config(config)
        
        # Mostrar mensagem de sucesso
        success_label = customtkinter.CTkLabel(
            window,
            text="✓ Configurações salvas com sucesso!", pady=5, padx=5,
            font=("Montserrat", 12, "bold"),
            text_color="#4aff4a"
        )
        success_label.pack(pady=5)
        window.after(2000, success_label.destroy)  # Remove após 2 segundos
    
    # Botão Salvar
    save_button = customtkinter.CTkButton(
        window,
        text="💾 Salvar Configurações",
        command=save_changes,
        fg_color="#4a9eff",
        hover_color="#3a8eef",
        font=("Montserrat", 13, "bold"),
        width=250,
        height=45,
        corner_radius=10
    )
    save_button.pack(pady=15)