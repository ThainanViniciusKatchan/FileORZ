import os
import sys
import subprocess
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import *
from time import sleep

# Pasta de saída para as builds
# exit folder to build
OUTPUT_DIR = "FileORZ"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def alterar_Config():
    print("\nAlterando config.json...")
    
    config = load_config()
    config["timeverification"] = "5"
    config['Startup'] = False
    config['Folder'] = 'pasta de organização'
    save_config(config)
    print("\nConfig.json alterado com sucesso")

# clean before build
def limpar_builds_anteriores():
    print("\nLimpando builds anteriores...")

    DeletarDados = ['build', OUTPUT_DIR, '__pycache__', 'index.build', 'index.dist', 
              'FileORZ.build', 'FileORZ.dist', 'FL_ORZ.build', 'FL_ORZ.dist']
    
    for Dados in DeletarDados:
        pasta_path = os.path.join(BASE_DIR, Dados)
        if os.path.exists(pasta_path):
            try:
                shutil.rmtree(pasta_path)
                print(f"  ✓ Pasta {Dados} removida")
            except Exception as e:
                print(f"  ⚠️ Erro ao remover {Dados}: {e}")
    
    # Remover arquivos .cmd gerados pelo Nuitka
    for arquivo in os.listdir(BASE_DIR):
        if arquivo.endswith('.cmd') or arquivo.endswith('.pyi'):
            try:
                os.remove(os.path.join(BASE_DIR, arquivo))
                print(f"  ✓ Arquivo {arquivo} removido")
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
        print(f"  ✓ FL_ORZ.exe movido para {OUTPUT_DIR}/")
    
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
        print(f"  ✓ FileORZ.exe movido para {OUTPUT_DIR}/dist/")

# copy config.json to ./dist/
def copiar_arquivos():
    print("\nCopiando config.json...")
    
    config_origem = os.path.join(BASE_DIR, 'dist', 'config.json')
    config_destino = os.path.join(BASE_DIR, OUTPUT_DIR, 'dist', 'config.json')
    
    if os.path.exists(config_origem):
        os.makedirs(os.path.dirname(config_destino), exist_ok=True)
        shutil.copy(config_origem, config_destino)
        print(f"  ✓ config.json copiado para {OUTPUT_DIR}/dist/")
    else:
        print(f"  ⚠️ config.json não encontrado em {config_origem}")

    print("\nCopiando changelog...")
    changelog_origem = os.path.join(BASE_DIR, 'changelog')
    changelog_destino = os.path.join(BASE_DIR, OUTPUT_DIR, 'changelog')
    
    if os.path.exists(changelog_origem):
        if os.path.exists(changelog_destino):
            shutil.rmtree(changelog_destino)
        shutil.copytree(changelog_origem, changelog_destino)
        print(f"Pasta changelog copiada para {OUTPUT_DIR}/")
    else:
        print(f"Pasta changelog não encontrada em {changelog_origem}")

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

# main
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Compilando FileORZ")
    print("=" * 50)
    sleep(2)

    alterar_Config()
    limpar_builds_anteriores()
    criar_pasta_build()
    
    if not compilar_organizador():
        print("\nFalha na compilação do organizador!")
        exit(1)
    
    if not compilar_ui():
        print("\nFalha na compilação da UI!")
        exit(1)
    
    reorganizar_estrutura()
    copiar_arquivos()
    limpar_temporarios()
    
    # Structure of files after build
    print("\n" + "=" * 50)
    print("\nCompilação concluída com sucesso!")
    print("=" * 50)
    print(f"\nEstrutura criada:")
    print(f"   {OUTPUT_DIR}/")
    print(f"   ├── FL_ORZ.exe     (UI Principal)")
    print(f"   └── dist/")
    print(f"       ├── FileORZ.exe    (Organizador)")
    print(f"       └── config.json    (Configurações)")
    print(f"   └── changelog/")
    print(f"       └── changelog.md   (Histórico de Versões)")
    print("=" * 50)