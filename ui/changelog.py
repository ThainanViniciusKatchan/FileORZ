import customtkinter as ctk
from tkinter import filedialog
import os
import sys
from centralizeWindow import centralize_window
import webbrowser
from CTkMessagebox import CTkMessagebox

def show_custom_changelog():
    url = "https://thainanviniciuskatchan.github.io/FileORZ/changelog.html"
    webbrowser.open(url)

if __name__ == "__main__":
    show_custom_changelog()