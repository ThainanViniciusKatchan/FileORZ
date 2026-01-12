import customtkinter
from customtkinter import filedialog
import os
import sys
from config import open_config_window
from header import header
from centralizeWindow import centralize_window
import ctypes

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import load_config, save_config, get_current_folder, get_time_verification, set_time_verification
from utils.StartTask import start_task, check_if_running

# Padrão de cores
COLORS = {
    "bg_primary": "#0D0D0D",
    "bg_secondary": "#1A1A2E",
    "bg_card": "#16213E",
    "accent_primary": "#9D4EDD",
    "accent_hover": "#7B2CBF",
    "accent_success": "#06D6A0",
    "accent_success_hover": "#05B88A",
    "text_primary": "#FFFFFF",
    "text_secondary": "#A0A0A0",
    "text_muted": "#6C6C6C",
    "border": "#2D2D44",
    "button_secondary": "#2D2D44",
    "button_secondary_hover": "#3D3D54",
    "dropdown_bg": "#1A1A2E",
}

ORZ = 'FLORZ'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(ORZ)

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    icon_path = os.path.join("ui", "icon", "IconApp.ico")
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join("ui", "icon", "IconApp.ico")

root = customtkinter.CTk()
root.title("File ORZ")
root.iconbitmap(default=icon_path)
root.geometry("700x420")
root.configure(fg_color=COLORS["bg_primary"])
root.resizable(False, False)

# Header
header(root)
# Centralizar janela na tela
centralize_window(root, 700, 420)

main_container = customtkinter.CTkFrame(root, fg_color="transparent")
main_container.pack(fill="both", expand=True, padx=30, pady=20)

folder_card = customtkinter.CTkFrame(
    main_container,
    fg_color=COLORS["bg_secondary"],
    corner_radius=12,
    border_width=1,
    border_color=COLORS["border"]
)
folder_card.pack(fill="x", pady=(0, 15))

folder_inner = customtkinter.CTkFrame(folder_card, fg_color="transparent")
folder_inner.pack(fill="x", padx=20, pady=15)

# Ícone e título
folder_header = customtkinter.CTkFrame(folder_inner, fg_color="transparent")
folder_header.pack(fill="x")

folder_icon = customtkinter.CTkLabel(
    folder_header,
    text="📂",
    font=customtkinter.CTkFont(size=18)
)
folder_icon.pack(side="left")

folder_title = customtkinter.CTkLabel(
    folder_header,
    text="Pasta para Organizar",
    font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
    text_color=COLORS["text_primary"]
)
folder_title.pack(side="left", padx=(8, 0))

# Botão selecionar pasta
def select_path():
    """Abre diálogo para selecionar pasta a ser organizada"""
    current_folder = get_current_folder()
    initial_dir = current_folder if os.path.exists(current_folder) else os.getcwd()
    
    selected_folder = filedialog.askdirectory(title="Selecione a pasta", initialdir=initial_dir)

    if selected_folder:
        config = load_config()
        config["Folder"] = selected_folder
        save_config(config)
        # Atualiza o label com o caminho
        folder_path_label.configure(text=selected_folder)
        print(f'Pasta salva com sucesso: {selected_folder}')
    else:
        print('Nenhuma pasta selecionada')

btn_Select_Folder = customtkinter.CTkButton(
    folder_header, 
    text="Selecionar",
    command=select_path, 
    fg_color=COLORS["button_secondary"],
    hover_color=COLORS["button_secondary_hover"],
    border_width=0,
    corner_radius=8, 
    font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
    width=120, 
    height=32
)
btn_Select_Folder.pack(side="right")

# Label mostrando caminho atual
current_folder = get_current_folder()
folder_path_label = customtkinter.CTkLabel(
    folder_inner,
    text=current_folder if current_folder else "Nenhuma pasta selecionada",
    font=customtkinter.CTkFont(family="Segoe UI", size=11),
    text_color=COLORS["text_secondary"],
    anchor="w"
)
folder_path_label.pack(fill="x", pady=(10, 0))

time_card = customtkinter.CTkFrame(
    main_container,
    fg_color=COLORS["bg_secondary"],
    corner_radius=12,
    border_width=1,
    border_color=COLORS["border"]
)
time_card.pack(fill="x", pady=(0, 15))

time_inner = customtkinter.CTkFrame(time_card, fg_color="transparent")
time_inner.pack(fill="x", padx=20, pady=15)

# Header do card
time_header = customtkinter.CTkFrame(time_inner, fg_color="transparent")
time_header.pack(fill="x")

time_icon = customtkinter.CTkLabel(
    time_header,
    text="⏱️",
    font=customtkinter.CTkFont(size=18)
)
time_icon.pack(side="left")

time_title = customtkinter.CTkLabel(
    time_header,
    text="Intervalo de Verificação (Segundos)",
    font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
    text_color=COLORS["text_primary"]
)
time_title.pack(side="left", padx=(8, 0))

# Configuração do tempo de verificação
time_value = get_time_verification()
if time_value != "5" or not time_value:
    DropDownTimeValue = customtkinter.StringVar(value=time_value)
else:
    DropDownTimeValue = customtkinter.StringVar(value="5")

set_time_verification(time_value)

# Dropdown do tempo
DropDownTime = customtkinter.CTkOptionMenu(
    time_header,
    fg_color=COLORS["dropdown_bg"],
    button_color=COLORS["accent_primary"],
    button_hover_color=COLORS["accent_hover"],
    text_color=COLORS["text_primary"],
    height=32,
    width=100,
    font=customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold"),
    dropdown_fg_color=COLORS["dropdown_bg"],
    dropdown_text_color=COLORS["text_primary"],
    dropdown_hover_color=COLORS["accent_hover"],
    variable=DropDownTimeValue,
    command=lambda x: set_time_verification(x),
    values=["5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"],
    dynamic_resizing=False,
    corner_radius=8
)
DropDownTime.pack(side="right")

# Descrição
time_desc = customtkinter.CTkLabel(
    time_inner,
    text="Tempo em segundos entre cada verificação automática de novos arquivos",
    font=customtkinter.CTkFont(family="Segoe UI", size=11),
    text_color=COLORS["text_secondary"],
    anchor="w"
)
time_desc.pack(fill="x", pady=(10, 0))

actions_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
actions_frame.pack(fill="x", pady=(10, 0))

# Botão de configurações (esquerda)
btn_config = customtkinter.CTkButton(
    actions_frame, 
    text="⚙️  Configurações",
    command=lambda: open_config_window(root),
    fg_color=COLORS["button_secondary"],
    hover_color=COLORS["button_secondary_hover"],
    border_width=0, 
    corner_radius=10, 
    font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
    width=160,
    height=42
)
btn_config.pack(side="left")

# Label de feedback
feedback_label = None

# Iniciar a organização
def start_organizer():
    global feedback_label
    
    config = load_config()
    folder = config.get("Folder", "")
    
    # Remove label anterior se existir
    if feedback_label is not None:
        feedback_label.destroy()

    STATUS = check_if_running("FileORZ.exe")

    if not folder or folder == "pasta de organização":
        feedback_label = customtkinter.CTkLabel(
            main_container,
            text="Selecione uma pasta primeiro!",
            font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="red"
        )
        feedback_label.pack(pady=(15, 0))
        root.after(3000, lambda: feedback_label.destroy() if feedback_label.winfo_exists() else None)
        return
    else:
        if start_task():
            feedback_label = customtkinter.CTkLabel(
                main_container,
                text="Organização concluída com sucesso!",
                font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color="green"
            )
            feedback_label.pack(pady=(15, 0))
            root.after(3000, lambda: feedback_label.destroy() if feedback_label.winfo_exists() else None)

    if STATUS:
        feedback_label = customtkinter.CTkLabel(
            main_container,
            text="Erro ao iniciar o organizador!",
            font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="red"
        )
        feedback_label.pack(pady=(15, 0))
        root.after(3000, lambda: feedback_label.destroy() if feedback_label.winfo_exists() else None)

# Botão para iniciar a organização
btn_Start_Organizer = customtkinter.CTkButton(
    actions_frame, 
    text="🚀  Iniciar Organização",
    command=start_organizer, 
    fg_color=COLORS["accent_success"],
    hover_color=COLORS["accent_success_hover"],
    corner_radius=10,
    border_width=0, 
    font=customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold"),
    width=200,
    height=48
)
btn_Start_Organizer.pack(side="right")

footer = customtkinter.CTkLabel(
    root,
    text="File ORZ - Organize seus arquivos",
    font=customtkinter.CTkFont(family="Segoe UI", size=10),
    text_color=COLORS["text_muted"]
)
footer.pack(side="bottom", pady=10)

root.resizable(False, False)
root.mainloop()