import os
import sys

# Pega o caminho do arquivo .exe se existir um 
def get_exe_path():
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        python_path = sys.executable
        script_path = os.path.dirname(os.path.abspath(__file__))
        return f'{python_path} {script_path}'

# Adiciona o atalho ao startup
def add_to_startup():
    # executa três metodos para adicionar o atalho ao startup
    try:
        startup_folder = os.path.join(os.getenv('APPDATA'), 
        r'Microsoft\Windows\Start Menu\Programs\Startup')
    
        shortcut_path = os.path.join(startup_folder, 'FileORZ.lnk')

        executable_path = get_exe_path()
    
        # Tenta adicionar o atalho ao startup usando o winshell
        try:
            import winshell
            with winshell.shortcut(shortcut_path) as shortcut:
                shortcut.path = executable_path
                shortcut.description = "Organiza arquivos automaticamente"
                shortcut.icon = "" 
            return True
        except:
            try:
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = executable_path
                shortcut.WorkingDirectory = os.path.dirname(executable_path)
                shortcut.save()
                return True
            except:
                # Tenta adicionar o atalho ao startup usando o Dispatch, adiciona um arquivo .bat com comando para iniciar o script
                bat_content = f'start "" {executable_path}'
                bat_path = os.path.join(startup_folder, 'FileORZ.bat')
                with open(bat_path, 'w') as f:
                    f.write(bat_content)
                return True
    except:
        print("Erro ao criar atalho")
        return False 
    


def remove_from_startup():
    startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    shortcut_path = os.path.join(startup_folder, 'FileORZ.lnk')
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
    return not os.path.exists(shortcut_path)
