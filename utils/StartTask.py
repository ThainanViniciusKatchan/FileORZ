from tkinter import messagebox
import os
import ctypes
import psutil
import customtkinter
from tkinter import messagebox
from utils import StartUp
from FileORZ import *
import subprocess


def check_if_running(taskname):
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == taskname:
            return True
    return False


def start_task():
    try:
        organize_files()
    except Exception as Error:
        print(f"Erro ao iniciar o Organizador: {Error}")
        return False
    return True


def close_task():
    STATUS = check_if_running("FL_ORZ.exe")
    if STATUS:
        subprocess.run(["taskkill", "/f", "/im", "FileORZ.exe"], check=True)


# Iniciar a organização
def start_organizer(main_container, root, folder, feedback_label):
    # Remove label anterior se existir
    if feedback_label is not None:
        feedback_label.destroy()

    # verifica se a pasta foi selecionada
    if not folder or folder == "pasta de organização":
        feedback_label = customtkinter.CTkLabel(
            main_container,
            text="Selecione uma pasta primeiro!",
            font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="red",
        )
        feedback_label.pack(pady=(15, 0))
        root.after(
            3000,
            lambda: feedback_label.destroy() if feedback_label.winfo_exists() else None,
        )
        return
    else:
        if start_task():
            feedback_label = customtkinter.CTkLabel(
                main_container,
                text="Organização concluída com sucesso!",
                font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color="green",
            )
            feedback_label.pack(pady=(15, 0))
            root.after(
                3000,
                lambda: (
                    feedback_label.destroy() if feedback_label.winfo_exists() else None
                ),
            )
        else:
            feedback_label = customtkinter.CTkLabel(
                main_container,
                text="Erro ao iniciar o organizador!",
                font=customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color="red",
            )
            feedback_label.pack(pady=(15, 0))
            root.after(
                3000,
                lambda: (
                    feedback_label.destroy() if feedback_label.winfo_exists() else None
                ),
            )

    # verifica se o processo do organizador já está funcionando
