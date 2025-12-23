import customtkinter
from customtkinter import filedialog
import os
import json
from config import open_config_window

# Caminho do arquivo de configuração
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
root.geometry("600x250")
root.configure(fg_color="#121212")
root.resizable(False, False)

# Abrir configurações
btn_config = customtkinter.CTkButton(
    root, 
    text="⚙️ Configurações",
    command=lambda: open_config_window(root),
    fg_color="#363636", 
    border_width=0, 
    corner_radius=20, 
    font=("Montserrat", 11, "bold"), 
    width=150, 
    hover_color="#0F0F0F"
)
btn_config.pack(pady=10, side="right", padx=20)


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
    text="📂 Selecionar pasta", 
    command=select_path, 
    fg_color="#363636", 
    border_width=0, 
    corner_radius=20, 
    font=("Montserrat", 11, "bold"), 
    width=150, 
    hover_color="#0F0F0F"
)

btn_Select_Folder.pack(pady=10, side="left", padx=20)

def start_organizer():
    config = load_config()
    folder = config.get("Folder", "")
    
    if not folder:
        success_label = customtkinter.CTkLabel(
            root,
            text="✓ Nenhuma pasta selecionada!", pady=5, padx=5,
            font=("Montserrat", 12, "bold"),
            text_color="#4aff4a"
        )
        root.after(2000, success_label.destroy)
        return

    success_label = customtkinter.CTkLabel(
        root,
        text="✓ Organização concluída!", pady=5, padx=5,
        font=("Montserrat", 12, "bold"),
        text_color="#4aff4a"
    )
    root.after(2000, success_label.destroy)

btn_Start_Organizer = customtkinter.CTkButton(
    root, 
    text="🗂️ Iniciar organização", 
    command=start_organizer, 
    fg_color="green", 
    border_width=0, 
    corner_radius=20, 
    font=("Montserrat", 11, "bold"), 
    width=150, 
    hover_color="#0F0F0F"
)
btn_Start_Organizer.pack(side=customtkinter.BOTTOM, pady=50)

def time_verification(time):
    print(time)
    config = load_config()
    config["timeverification"] = time
    save_config(config)
    return time

DropDownTimeValue = customtkinter.StringVar(value="5")
DropDownTime = customtkinter.CTkOptionMenu(
    root,
    variable=DropDownTimeValue,
    values=["5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"],
    command=time_verification
)

time_verification = time_verification(DropDownTimeValue.get())
DropDownTime.pack(pady=50,
side=customtkinter.TOP)


root.resizable(False, False)
root.mainloop()
