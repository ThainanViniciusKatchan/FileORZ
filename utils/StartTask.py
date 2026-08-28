import os
import psutil
import customtkinter
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from FileORZ import organize_files, loop_verification


def check_if_running(taskname):
    try:
        for proc in psutil.process_iter(["name"]):
            name = proc.info.get("name")
            if name and name.lower() == taskname.lower():
                return True
    except Exception:
        pass
    return False


def start_task():
    import json
    from utils.model import json_path
    import threading

    CONFIG_PATH = json_path("dist", "config")
    try:
        print("Iniciando a organização...")
        thread = threading.Thread(target=loop_verification, daemon=True)
        thread.start()

        rtn = True
    except Exception as Error:
        print(f"Erro ao iniciar o Organizador: {Error}")
        rtn = False

    return rtn


def close_task():
    processos = ["FL_ORZ.exe", "FileORZ.exe"]
    for proc in processos:
        if check_if_running(proc):
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", proc, "/T"],
                    capture_output=True,
                    check=False,
                )
            except Exception as Error:
                print(f"Erro ao encerrar processo {proc}: {Error}")


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


if __name__ == "__main__":
    start_task()
