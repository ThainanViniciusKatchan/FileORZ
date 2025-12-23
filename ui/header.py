import customtkinter
import webbrowser
import os 
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import get_startup, set_startup
from utils.startupfile import add_to_startup, remove_from_startup

def header(root):
    header_frame = customtkinter.CTkFrame(root, fg_color="#3A70B8", corner_radius=0, height=50)
    header_frame.pack(fill="x", side="top")
    git = git_button(header_frame)
    startup = startup_button(header_frame)
    startup.pack(pady=10, padx=20, side="right", anchor="center")
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
    
    def on_checkbox_toggle():
        if startup_var.get():
            success = add_to_startup()
            if not success:
                # Se falhar, desmarca o checkbox
                startup_var.set(False)
                print("Erro ao adicionar à inicialização")
        else:
            remove_from_startup()
    
    btn_Enable_Startup = customtkinter.CTkCheckBox(
        header_frame,
        text="🪟 Iniciar com o windows",
        variable=startup_var,
        command=on_checkbox_toggle,
        fg_color="#363636",
        corner_radius=0,
        border_width=2,
        font=("Montserrat", 11, "bold"),
        width=50,
    )
    
    return btn_Enable_Startup
    