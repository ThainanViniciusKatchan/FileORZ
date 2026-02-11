import customtkinter as ctk
from tkinter import filedialog
import os
import sys
import webbrowser
from CTkMessagebox import CTkMessagebox

# open changelog
def abrir_changelog():
    url = "https://thainanviniciuskatchan.github.io/FileORZ/changelog.html"
    webbrowser.open(url)

if __name__ == "__main__":
    abrir_changelog()