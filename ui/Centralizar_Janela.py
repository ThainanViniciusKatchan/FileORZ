import customtkinter as ctk

# centralize window
def Centralizar_Janela(window, width, height):
    window.update_idletasks()
    
    width_screen = window.winfo_screenwidth()
    height_screen = window.winfo_screenheight()
    
    x = int((width_screen / 2) - (width / 2))
    y = int((height_screen / 2) - (height / 2))

    window.geometry(f"{width}x{height}+{x}+{y}")
    return window
