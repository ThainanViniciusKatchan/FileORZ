import customtkinter
import webbrowser

def header(root):
    header_frame = customtkinter.CTkFrame(root, fg_color="#3A70B8", corner_radius=0, height=50)
    header_frame.pack(fill="x", side="top")
    git = git_button(header_frame)
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
    cursor = "hand2"
    git_button.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/ThainanViniciusKatchan/FileORZ"))
    return git_button