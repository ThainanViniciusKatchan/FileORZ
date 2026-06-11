import os
import psutil
import customtkinter
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from FileORZ import organize_files


def check_if_running(taskname):
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == taskname:
            return True
    return False


def start_task():
    from time import sleep
    import json
    from utils.model import json_path

    CONFIG_PATH = json_path("dist", "config")
    try:
        print("Iniciando FileORZ Organizer...")
        while True:
            organize_files()

            # Ler o tempo de verificação a cada ciclo para permitir atualizações em tempo real
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                time_verification = float(data.get("timeverification", 5))
            except (FileNotFoundError, json.JSONDecodeError, ValueError):
                time_verification = 5

            print(
                f"\nAguardando {time_verification} minutos para a próxima verificação..."
            )
            sleep(time_verification * 60)
        rtn = True
    except Exception as Error:
        print(f"Erro ao iniciar o Organizador: {Error}")
        rtn = False

    return rtn


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
        if start_task() is True:
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
