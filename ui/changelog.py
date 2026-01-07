import customtkinter as ctk
from tkinter import filedialog
import os
import sys
from centralizeWindow import centralize_window

def open_changelog():
    # Configurar aparência (pode ser ajustado conforme seu tema)
    ctk.set_appearance_mode("dark")  # "dark", "light", "system"
    ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
    
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    file_path = os.path.join(application_path, "changelog", "changelog.md")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            # Criar janela personalizada
            show_custom_changelog(text)
            
        except Exception as e:
            ctk.CTkMessageBox(title="Erro", 
                             text=f"Não foi possível ler o changelog:\n{e}",
                             icon="cancel")
    else:
        ctk.CTkMessageBox(title="Erro", 
                         text="Arquivo de changelog não encontrado.",
                         icon="cancel")

def show_custom_changelog(text):
    # Criar uma nova janela
    changelog_window = ctk.CTkToplevel()
    changelog_window.title("Changelog")
    changelog_window.geometry("700x550")
    changelog_window.resizable(False, False)
    centralize_window(changelog_window, 700, 550)
    
    # Definir cores personalizadas
    changelog_window.configure(fg_color="#2b2b2b")  # Cor de fundo da janela
    
    # Tornar a janela modal (bloqueia a janela principal)
    changelog_window.grab_set()
    
    # Frame principal com padding
    main_frame = ctk.CTkFrame(changelog_window, fg_color="#2b2b2b")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
    title_label = ctk.CTkLabel(main_frame, 
                               text="Changelog",
                               font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=(0, 10))
    
    # Frame para o texto com scrollbar
    text_frame = ctk.CTkFrame(main_frame)
    text_frame.pack(fill="both", expand=True)
    
    # Text widget com scrollbar
    text_widget = ctk.CTkTextbox(text_frame,
                                 wrap="word",
                                 font=ctk.CTkFont(family="Consolas", size=12),
                                 fg_color="#1e1e1e",
                                 text_color="#ffffff")
    
    text_widget.pack(side="left", fill="both", expand=True)

    # Inserir texto
    text_widget.insert("1.0", text)
    text_widget.configure(state="disabled")  # Somente leitura
    
    # Botão de fechar
    close_button = ctk.CTkButton(main_frame,
                                 text="Fechar",
                                 command=changelog_window.destroy,
                                 width=100)
    close_button.pack(pady=(10, 0))
    
    # Centralizar na tela
    changelog_window.update_idletasks()
    width = changelog_window.winfo_width()
    height = changelog_window.winfo_height()
    x = (changelog_window.winfo_screenwidth() // 2) - (width // 2)
    y = (changelog_window.winfo_screenheight() // 2) - (height // 2)
    changelog_window.geometry(f'{width}x{height}+{x}+{y}')

    # Iniciar o loop principal
    changelog_window.mainloop()

if __name__ == "__main__":
    open_changelog()