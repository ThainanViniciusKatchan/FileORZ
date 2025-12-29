import customtkinter
import webbrowser

def header(root):
    # Usando Slate 800 para o header para diferenciar levemente do fundo principal (Slate 900)
    header_frame = customtkinter.CTkFrame(root, fg_color="#1e293b", corner_radius=0, height=60)
    header_frame.pack(fill="x", side="top")
    
    # Grid layout para melhor controle
    header_frame.grid_columnconfigure(0, weight=1)
    header_frame.grid_columnconfigure(1, weight=0)

    # Logo/Título com fonte moderna
    header_label = customtkinter.CTkLabel(
        header_frame, 
        text="FileORZ",
        font=customtkinter.CTkFont(family="Roboto", size=24, weight="bold"),
        text_color="#f1f5f9" # Slate 100
    )
    header_label.pack(side="left", padx=25, pady=15)
    
    # Botão Github modernizado
    git = git_button(header_frame)
    git.pack(side="right", padx=25, pady=15)
    
    return header_frame

def git_button(header_frame):
    git_button = customtkinter.CTkButton(
        header_frame, 
        text="GitHub",
        font=customtkinter.CTkFont(family="Roboto", size=13, weight="bold"),
        fg_color="#334155", # Slate 700
        text_color="#f8fafc", # Slate 50
        border_width=0, 
        corner_radius=8,
        height=32,
        width=100,
        hover_color="#475569" # Slate 600
    )
    
    # Adicionando ícone se possível ou mantendo texto limpo
    # Por enquanto texto limpo com hover effect melhor
    
    git_button.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/ThainanViniciusKatchan/FileORZ"))
    return git_button
