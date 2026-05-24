"""
    Copyright (C) 2026 Thainan Vinicius Katchan

    This file is part of FileORZ.

    FileORZ is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    FileORZ is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with FileORZ.  If not, see <https://www.gnu.org/licenses/
"""

import customtkinter
import os
import sys
import subprocess

from ui.header import header
from ui.Centralizar_Janela import Centralizar_Janela
from ui.Select_Folder import folder_select
from ui.Time_Select import time_select
from ui.btn import config_btn, start_btn
import ctypes

from utils import folder, timeVerification

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

Time = timeVerification
Folder = folder.Folder()

# Busca a pasta de execução da aplicação
if getattr(sys, "frozen", False):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(base_path, "icon", "IconApp.ico")

root = customtkinter.CTk()
root.title("File ORZ")

# Busca o Icone da aplicação
if os.path.exists(icon_path):
    root.iconbitmap(default=icon_path)
else:
    print(f"[AVISO] Ícone não encontrado em: {icon_path}")

root.geometry("700x420")
root.configure(fg_color=COLORS["bg_primary"])
root.resizable(False, False)
# Header
header(root)
# Centralize window
Centralizar_Janela(root, 700, 420)
main_container = customtkinter.CTkFrame(root, fg_color="transparent")
main_container.pack(fill="both", expand=True, padx=30, pady=20)

folder_select(main_container, COLORS) # Select Folder
time_select(main_container, COLORS) # Select time

actions_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
actions_frame.pack(fill="x", pady=(10, 0))

# Label de feedback
feedback_label = None

# btn
config_btn(COLORS, actions_frame, root) # Config btn
start_btn(COLORS, actions_frame) # Start btn

# Rodapé
footer = customtkinter.CTkLabel(
    root,
    text="File ORZ - Organize seus arquivos",
    font=customtkinter.CTkFont(family="Segoe UI", size=10),
    text_color=COLORS["text_muted"]
)
footer.pack(side="bottom", pady=10)

def restore_windows():
    root.after(0, root.deiconify)

def on_app():
    root.mainloop()
    root.deiconify()
    root.lift()
    root.attributes('-topmost', True)

def close_process(): # Fecha o app quando clicar no X
    try:
        meu_icone.stop()
        root.destroy()
        subprocess.run(['taskkill', '/f', '/im', "FL_ORZ.exe"], capture_output=True)
    except Exception as Error:
        print(f"Aviso - Erro ao matar o processo FL_ORZ: {Error}")

def close_app():
    root.withdraw()

root.protocol("WM_DELETE_WINDOW", close_app)
# Icone no SysTray do Windows
from utils.system_tray import fila_comandos, meu_icone, image_icon
import queue
from ui.index import actions_frame

def verificar_fila():
    try:
        # Pega a mensagem da fila
        comando = fila_comandos.get_nowait()

        # Abre a janela de acordo com a mensagem, na thread certa!
        if comando == "abrir_Index":
            restore_windows()
        elif comando == "fechar_app":
            close_process()

    except queue.Empty:
        pass

    # Manda checar de novo daqui a 100 milissegundos
    actions_frame.after(100, verificar_fila)

# Dá o pontapé inicial na checagem antes de abrir o app
if root.winfo_exists():
    verificar_fila()
    meu_icone.run_detached()

if __name__ == "__main__":
    on_app()
