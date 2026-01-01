import customtkinter
import webbrowser
import os 
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import get_startup, set_startup, is_startup_enabled, toggle_startup as toggle_startup_registry

def header(root):
    header_frame = customtkinter.CTkFrame(root, fg_color="#3A70B8", corner_radius=0, height=50)
    header_frame.pack(fill="x", side="top")
    git = git_button(header_frame)
    startup_switch = startup_button(header_frame)
    startup_switch.pack(pady=10, padx=20, side="right", anchor="center")
    git.pack(pady=10, padx=20, side="right", anchor="center")
    header_label = customtkinter.CTkLabel(header_frame, text="FileORZ",
    font=customtkinter.CTkFont(size=20, weight="bold", slant="italic", underline=True))
    header_label.pack(pady=10, padx=20, side="left", anchor="center")
    
    return header_frame

def git_button(header_frame):
    git_button = customtkinter.CTkButton(header_frame, text="🐈 GitHub",
    font=customtkinter.CTkFont(size=12, weight="bold"),
    fg_color="#363636", 
    border_width=0, 
    corner_radius=20,
    height=25,
    hover_color="#0F0F0F")
    git_button.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/ThainanViniciusKatchan/FileORZ"))
    return git_button


def startup_button(header_frame):

    startup_var = customtkinter.BooleanVar(value=get_startup())

    def on_toggle():
        is_enabled = startup_var.get()
        # Atualiza o config.json
        set_startup(is_enabled)
        # Cria ou remove o registro do Windows
        toggle_startup_registry(is_enabled)

    startup_switch = customtkinter.CTkSwitch(
        header_frame, 
        text="🪟 Iniciar com o Windows",
        command=on_toggle,
        variable=startup_var,
        font=("Montserrat", 12, "bold"),
        fg_color="#363636",
        progress_color="#4a9eff"
    )

    return startup_switch   

    
    