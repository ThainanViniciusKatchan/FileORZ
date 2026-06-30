from PIL import Image

# pyrefly: ignore [missing-import]
from pystray import MenuItem as item, Icon as icon_class, Menu as menu
import queue
from os import path

fila_comandos = queue.Queue()

image_icon = Image.open(
    path.join(path.dirname("__file__"), "ui", "icon", "IconApp.ico")
)


def open_condfig(icon, item):
    fila_comandos.put("abrir_Index")


def open_autodell(icon, item):
    fila_comandos.put("fechar_app")


meu_icone = icon_class(
    "File_ORZ",
    image_icon,
    "FileORZ",
    menu=menu(item("Abrir", open_condfig), item("Fechar", open_autodell)),
)
