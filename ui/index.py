import customtkinter
from customtkinter import filedialog
import os
import sys
from config import open_config_window
from header import header
from centralizeWindow import centralize_window

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import load_config, save_config, get_current_folder, get_time_verification, set_time_verification
from utils.StartTask import start_task

# Caminho do ícone
icon_dir = os.path.join(os.path.dirname(__file__), "icon")
icon_path = os.path.join(icon_dir, "IconApp.ico")

root = customtkinter.CTk()
root.title("FileORZ")

# Tentar definir ícone
try:
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
except Exception:
    pass  # Ignora se não conseguir carregar o ícone
root.geometry("600x300")
root.configure(fg_color="#121212")
root.resizable(False, False)
header(root)
centralize_window(root, 600, 300)

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

# Selecionar pasta para organizar
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

# Iniciar a organização
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
    else:
        start_task()
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
    fg_color="#194036",
    hover_color="#1D4D40",
    corner_radius=20,
    border_width=0, 
    font=("Montserrat", 11, "bold"), 
    width=150, 
)
btn_Start_Organizer.pack(side=customtkinter.BOTTOM, pady=50)

# Configuração do tempo de verificação
time_value = get_time_verification()
 # Valida se o valor é diferente de 5 ou se não existe, se caso ele existir ele pega o valor que foi salvo
if time_value != "5" or not time_value:
    DropDownTimeValue = customtkinter.StringVar(value=time_value)
else: # Se não ele seta o valor padrão que é 5
    DropDownTimeValue = customtkinter.StringVar(value="5")

set_time_verification(time_value)

# Criação do menu de tempo de verificação
DropDownTime = customtkinter.CTkOptionMenu(
    root,
    fg_color="#192F42",
    text_color="#FFFFFF",
    height=50,
    width=150,
    font=("Montserrat", 11, "bold"),
    dropdown_fg_color="#192F42",
    dropdown_text_color="#FFFFFF",
    variable=DropDownTimeValue,
    command=lambda x: set_time_verification(x),
    values=["5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"],
    dynamic_resizing=False,
)
time_verification = get_time_verification()
DropDownTime.pack(pady=50,
side=customtkinter.TOP)

root.resizable(False, False)
root.mainloop()