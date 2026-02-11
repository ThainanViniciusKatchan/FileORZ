import os
import sys
import subprocess
import shutil

# add path to utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import *
from time import sleep

# Pasta de saída para as builds
# exit folder to build
OUTPUT_DIR = "FileORZ"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# alter config.json
def alterar_Config():
    print("\nAlterando config.json...")
    config = load_config()
    config["timeverification"] = "5"
    config['Startup'] = False
    config['Folder'] = 'pasta de organização'
    save_config(config)
    print("\nConfig.json alterado com sucesso")

# clean previus build
def limpar_builds_anteriores():
    print("\nLimpando builds anteriores...")

    DeletarDados = ['build', OUTPUT_DIR, '__pycache__', 'index.build', 'index.dist', 
              'FileORZ.build', 'FileORZ.dist', 'FL_ORZ.build', 'FL_ORZ.dist']
    
    for Dados in DeletarDados:
        pasta_path = os.path.join(BASE_DIR, Dados)
        if os.path.exists(pasta_path):
            try:
                shutil.rmtree(pasta_path)
                print(f"  [OK] Pasta {Dados} removida")
            except Exception as e:
                print(f"  [ERRO] Erro ao remover {Dados}: {e}")
    
    # Remover arquivos .cmd gerados na build
    # remove files .cmd generated in build
    for arquivo in os.listdir(BASE_DIR):
        if arquivo.endswith('.cmd') or arquivo.endswith('.pyi'):
            try:
                os.remove(os.path.join(BASE_DIR, arquivo))
                print(f"  [OK] Arquivo {arquivo} removido")
            except:
                pass

# create build folder
def criar_pasta_build():
    print("\nCriando estrutura de pastas...")
    output_path = os.path.join(BASE_DIR, OUTPUT_DIR)
    dist_path = os.path.join(output_path, "dist")
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(dist_path, exist_ok=True)
    print(f"\nEstrutura {OUTPUT_DIR}/ e {OUTPUT_DIR}/dist/ criada")

# compile organizer (FileORZ.py)
def compilar_organizador():
    print("\nCompilando o organizador (FileORZ.py) com Nuitka...")
    
    os.chdir(BASE_DIR)
    
    dist_path = os.path.join(OUTPUT_DIR, "dist")
    
    comando = [
        sys.executable, '-m', 'nuitka',
        '--standalone',                          
        '--windows-console-mode=disable',
        f'--output-dir={dist_path}',
        '--output-filename=FileORZ.exe',         
        f'--windows-icon-from-ico=ui/icon/IconApp.ico',
        '--assume-yes-for-downloads',
        '--force-dll-dependency-cache-update',
        'FileORZ.py'
    ]
    
    print(f"Executando: {' '.join(comando)}")
    
    result = subprocess.run(comando, capture_output=False, text=True)
    
    if result.returncode == 0:
        print(f"\nOrganizador compilado com sucesso")
        return True
    else:
        print(f"Erro ao compilar organizador")
        return False

# compile ui all files in ./ui/
def compilar_ui():
    print("\nCompilando a UI (index.py) com Nuitka...")
    
    os.chdir(BASE_DIR)
    
    comando = [
        sys.executable, '-m', 'nuitka',
        '--standalone',                          
        '--windows-console-mode=disable',       
        f'--output-dir={OUTPUT_DIR}',            
        '--output-filename=FL_ORZ.exe',          
        f'--windows-icon-from-ico=ui/icon/IconApp.ico',  
        '--enable-plugin=tk-inter',              
        '--include-package=customtkinter',       
        '--include-package=PIL',                 
        '--include-package=darkdetect',          
        '--include-package=utils',               
        '--include-data-dir=ui=ui',              
        '--assume-yes-for-downloads',
        '--force-dll-dependency-cache-update',
        'ui/index.py'
    ]
    
    print(f"Executando: {' '.join(comando)}")
    
    result = subprocess.run(comando, capture_output=False, text=True)
    
    if result.returncode == 0:
        print(f"\nUI compilada com sucesso")
        return True
    else:
        print(f"Erro ao compilar UI")
        return False

# reorganize structure of files
def reorganizar_estrutura():
    print("\nReorganizando estrutura de arquivos...")
    
    output_path = os.path.join(BASE_DIR, OUTPUT_DIR)
    
    index_dist = os.path.join(output_path, "index.dist")
    if os.path.exists(index_dist):
        print(f"  Movendo arquivos de index.dist/ para {OUTPUT_DIR}/")
        for item in os.listdir(index_dist):
            origem = os.path.join(index_dist, item)
            destino = os.path.join(output_path, item)
            if os.path.exists(destino):
                if os.path.isdir(destino):
                    shutil.rmtree(destino)
                else:
                    os.remove(destino)
            shutil.move(origem, destino)
        shutil.rmtree(index_dist)
        print(f"  [OK] FL_ORZ.exe movido para {OUTPUT_DIR}/")
    
    fileorz_dist = os.path.join(output_path, "dist", "FileORZ.dist")
    dist_final = os.path.join(output_path, "dist")
    if os.path.exists(fileorz_dist):
        print(f"  Movendo arquivos de dist/FileORZ.dist/ para {OUTPUT_DIR}/dist/")
        for item in os.listdir(fileorz_dist):
            origem = os.path.join(fileorz_dist, item)
            destino = os.path.join(dist_final, item)
            if os.path.exists(destino):
                if os.path.isdir(destino):
                    shutil.rmtree(destino)
                else:
                    os.remove(destino)
            shutil.move(origem, destino)
        shutil.rmtree(fileorz_dist)
        print(f"  [OK] FileORZ.exe movido para {OUTPUT_DIR}/dist/")

# create default file config.json
def Criar_Config_Padrao():
    config = {
        "Desenvolvimento": {
        ".htm": True,
        ".html": True,
        ".cfg": True,
        ".alg": True,
        ".md": True,
        ".ftl": True,
        ".json": True,
        ".py": True,
        ".bat": True,
        ".cmd": True,
        ".ps1": True,
        ".sh": True,
        ".ini": True,
        ".js": True,
        ".ts": True,
        ".css": True,
        ".java": True,
        ".cpp": True,
        ".cs": True,
        ".php": True,
        ".c": True,
        ".net": True,
        ".pyd": True
    },
    "documentos": {
        ".pdf": True,
        ".doc": True,
        ".txt": True,
        ".pptx": True,
        ".docx": True,
        ".xlsx": True,
        ".xlsm": True,
        ".csv": True,
        ".xls": True,
        ".dotm": True,
        ".ponto": True,
        ".dotx": True,
        ".htm": True,
        ".html": True,
        ".cfg": True,
        ".alg": True,
        ".md": True,
        ".ftl": True
    },
    "videos": {
        ".mov": True,
        ".mp4": True,
        ".avi": True,
        ".av1": True,
        ".mpeg-2": True,
        ".avchd": True,
        ".aac": True,
        ".mkv": True,
        ".divx": True,
        ".h.264": True,
        ".mpeg-1": True,
        ".wmv": True
    },
    "audios": {
        ".mp3": True,
        ".wav": True,
        ".flac": True,
        ".3GP": True,
        ".M4A": True,
        ".ogg": True,
        ".wma": True,
        ".m4a": True,
        ".webm": True
    },
    "compactos": {
        ".rar": True,
        ".zip": True,
        ".zpix": True,
        ".7z": True,
        ".rar5": True,
        ".iso": True,
        ".gzip": True,
        ".7-zip": True,
        ".tar": True
    },
    "fontes": {
        ".ttf": True,
        ".eot": True,
        ".woff": True,
        ".woff2": True
    },
    "setups": {
        ".exe": True,
        ".msi": True,
        ".appx": True,
        ".appxbundle": True,
        ".msix": True,
        ".apk": True,
        ".Msixbundle": True
    },
    "imagens": {
        ".jpg": True,
        ".jpeg": True,
        ".png": True,
        ".bmp": True,
        ".tiff": True,
        ".gif": True,
        ".cr3": True,
        ".cr2": True,
        ".exif": True,
        ".psd": True,
        ".af": True,
        ".eps": True,
        ".ai": True,
        ".svg": True,
        ".webp": True,
        ".heic": True,
        ".heif": True,
        ".raw": True
    },
    "timeverification": "5",
    "Startup": False,
    "Folder": "pasta de organização"
    }
    
    BUILD_DIR = os.path.join(BASE_DIR, OUTPUT_DIR, 'dist', 'config.json')
    DIST_DIR = os.path.join(BASE_DIR, 'dist', 'config.json')

    paths = [BUILD_DIR, DIST_DIR]

    for path in paths:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
            print(f"config.json padrão criado em: {path}")
            sleep(2)
    
# clean temporary files
def limpar_temporarios():
    print("\nLimpando arquivos temporários...")
    
    os.chdir(BASE_DIR)

    pastas_temp = ['index.build', 'index.dist', 'index.onefile-build',
                   'FileORZ.build', 'FileORZ.dist', 'FileORZ.onefile-build']
    
    for pasta in pastas_temp:
        pasta_path = os.path.join(BASE_DIR, pasta)
        if os.path.exists(pasta_path):
            try:
                shutil.rmtree(pasta_path)
                print(f"Pasta {pasta} removida")
            except Exception as e:
                print(f"Erro ao remover {pasta}: {e}")

# Start build
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Compilando FileORZ")
    print("=" * 50)
    sleep(2)

    # stages of build
    ETAPAS = [
        ("limpar_builds_anteriores",limpar_builds_anteriores),
        ("criar_pasta_build",criar_pasta_build),
        ("compilar_ui",compilar_ui),
        ("compilar_organizador",compilar_organizador),
        ("reorganizar_estrutura",reorganizar_estrutura),
        ("Criar_Config_Padrao",Criar_Config_Padrao),
        ("alterar_Config",alterar_Config),
        ("limpar_temporarios",limpar_temporarios)
    ]

    print("Iniciando processo de compilação...\n")
    sleep(2)

    # execute stages
    for nome_etapa, etapa in ETAPAS:
        print(f"\nEtapa: {nome_etapa}")
        try:
            resultado = etapa()
        except Exception as e:
            print(f" 🛑 Erro na etapa {nome_etapa}: {e}")
            exit(1)

        print(f"\n ✅ Etapa {nome_etapa} concluída com sucesso!")
        sleep(2)
        print("\n" + "=" * 50)

    print("\n ✅ Compilação concluída com sucesso!")