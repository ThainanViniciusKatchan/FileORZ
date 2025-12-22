import customtkinter
from customtkinter import filedialog
import os
import json

# Caminho do arquivo de configuração
SCRIPT_DIR = os.path.dirname(os.path.abspath("config.json"))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

# Função para carregar a configuração
def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# Função para salvar a configuração
def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

# Carregar pasta atual salva
def get_current_folder():
    config = load_config()
    return config.get("Folder", "")

root = customtkinter.CTk()
root.title("FileORZ")
root.geometry("900x600")
root.configure(fg_color="#121212")

# Selecionar pasta de downloads
def select_path():
    # Abrir diálogo começando pela pasta atual salva (se existir)
    current_folder = get_current_folder()
    initial_dir = current_folder if os.path.exists(current_folder) else os.getcwd()
    
    selected_folder = filedialog.askdirectory(title="Selecione a pasta", initialdir=initial_dir)

    if selected_folder:
        # Carregar config atual, atualizar pasta e salvar
        config = load_config()
        config["Folder"] = selected_folder
        save_config(config)
        print(f'Pasta salva com sucesso: {selected_folder}')
    else:
        print('Nenhuma pasta selecionada')

btn_Select_Folder = customtkinter.CTkButton(
    root, 
    text="Selecionar pasta", 
    command=select_path, 
    fg_color="#363636", 
    border_width=0, 
    corner_radius=20, 
    font=("Montserrat", 10, "bold"), 
    width=150, 
    hover_color="#0F0F0F"
)

btn_Select_Folder.pack(pady=10, side="left", padx=20)
    
root.resizable(False, False)
root.mainloop()
