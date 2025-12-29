import customtkinter
from customtkinter import filedialog
import os
import sys
from config import open_config_window
from header import header
from centralizeWindow import centralize_window

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from FileORZ import organize_files
from model import load_config, save_config, get_current_folder, get_time_verification, set_current_folder, set_time_verification

# Configuração global de aparência
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.title("FileORZ")
# Aumentando um pouco a altura para acomodar o novo layout confortavelmente
root.geometry("700x500")
root.configure(fg_color="#0f172a") # Slate 900
root.resizable(False, False)

# Header
header(root)
centralize_window(root, 700, 500)

# Main Container
main_frame = customtkinter.CTkFrame(root, fg_color="transparent")
main_frame.pack(fill="both", expand=True, padx=40, pady=20)

# --- Seção de Status / Informação ---
info_frame = customtkinter.CTkFrame(main_frame, fg_color="#1e293b", corner_radius=15, border_width=1, border_color="#334155")
info_frame.pack(fill="x", pady=(0, 20))

info_label = customtkinter.CTkLabel(
    info_frame, 
    text="PASTA ATUAL", 
    font=customtkinter.CTkFont(family="Roboto", size=11, weight="bold"),
    text_color="#94a3b8" # Slate 400
)
info_label.pack(pady=(15, 0), anchor="center")

current_folder_var = customtkinter.StringVar(value="Nenhuma pasta selecionada")
path_label = customtkinter.CTkLabel(
    info_frame, 
    textvariable=current_folder_var,
    font=customtkinter.CTkFont(family="Roboto", size=14),
    text_color="#e2e8f0", # Slate 200
    wraplength=600
)
path_label.pack(pady=(5, 15), padx=20, anchor="center")

def update_folder_display():
    folder = get_current_folder()
    if folder and os.path.exists(folder):
        current_folder_var.set(folder)
    else:
        current_folder_var.set("Nenhuma pasta selecionada")

update_folder_display()

# --- Seção de Ações Principais ---
actions_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
actions_frame.pack(fill="both", expand=True)
actions_frame.grid_columnconfigure(0, weight=1)
actions_frame.grid_columnconfigure(1, weight=1)

# Botão Selecionar Pasta
def select_path():
    current = get_current_folder()
    initial = current if os.path.exists(current) else os.getcwd()
    selected = filedialog.askdirectory(title="Selecione a pasta para organizar", initialdir=initial)
    
    if selected:
        config = load_config()
        config["Folder"] = selected
        save_config(config)
        update_folder_display()
        # Feedback visual sutil (pode ser implementado aqui)

btn_select = customtkinter.CTkButton(
    actions_frame,
    text="Selecionar Pasta",
    command=select_path,
    fg_color="#3b82f6", # Blue 500
    hover_color="#2563eb", # Blue 600
    text_color="white",
    font=customtkinter.CTkFont(family="Roboto", size=14, weight="bold"),
    height=50,
    corner_radius=10,
    width=280
)
btn_select.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")

# Botão Configurações
btn_config = customtkinter.CTkButton(
    actions_frame,
    text="Configurações",
    command=lambda: open_config_window(root),
    fg_color="#334155", # Slate 700
    hover_color="#475569", # Slate 600
    text_color="white",
    font=customtkinter.CTkFont(family="Roboto", size=14, weight="bold"),
    height=50,
    corner_radius=10,
    width=280
)
btn_config.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="ew")

# Botão Iniciar Organização (Grande destaque)
def start_organizer():
    folder = get_current_folder()
    if not folder:
        # Erro visual na label
        current_folder_var.set("❌ Selecione uma pasta primeiro!")
        root.after(2000, update_folder_display)
        return
        
    try:
        organize_files()
        # Sucesso visual
        original_text = btn_start.cget("text")
        btn_start.configure(text="✓ Organizado com Sucesso!", fg_color="#10b981", hover_color="#059669")
        root.after(2000, lambda: btn_start.configure(text=original_text, fg_color="#3b82f6", hover_color="#2563eb"))
    except Exception as e:
        print(f"Erro: {e}")

btn_start = customtkinter.CTkButton(
    actions_frame,
    text="Organizar Arquivos Agora",
    command=start_organizer,
    fg_color="#3b82f6", # Blue 500
    hover_color="#2563eb", # Blue 600
    text_color="white",
    font=customtkinter.CTkFont(family="Roboto", size=16, weight="bold"),
    height=60,
    corner_radius=12
)
btn_start.grid(row=1, column=0, columnspan=2, pady=(20, 10), sticky="ew")

# --- Footer: Configuração de Tempo ---
footer_frame = customtkinter.CTkFrame(root, fg_color="#0f172a", height=60, corner_radius=0)
footer_frame.pack(fill="x", side="bottom")

time_label = customtkinter.CTkLabel(
    footer_frame,
    text="Verificação Automática (Segundos):",
    font=customtkinter.CTkFont(family="Roboto", size=12),
    text_color="#94a3b8"
)
time_label.pack(side="left", padx=(40, 10), pady=20)

time_value = get_time_verification()
current_time = "5" if (not time_value or time_value == "5") else time_value
set_time_verification(current_time) # Garantir valor válido

time_var = customtkinter.StringVar(value=current_time)

def on_time_change(choice):
    set_time_verification(choice)

time_menu = customtkinter.CTkOptionMenu(
    footer_frame,
    values=[str(i) for i in range(5, 65, 5)],
    variable=time_var,
    command=on_time_change,
    fg_color="#1e293b",
    button_color="#334155",
    button_hover_color="#475569",
    text_color="white",
    width=80,
    corner_radius=8
)
time_menu.pack(side="left", pady=20)

root.mainloop()
