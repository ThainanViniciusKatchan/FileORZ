import os
import subprocess
import shutil
import time

# Pasta de saída para as builds
OUTPUT_DIR = "FileORZ"

def limpar_builds_anteriores():
    """Limpa todas as pastas de build anteriores"""
    print("\n🧹 Limpando builds anteriores...")
    
    pastas = ['build', 'build_ui', 'build_orz', OUTPUT_DIR, '__pycache__']
    
    for pasta in pastas:
        if os.path.exists(pasta):
            try:
                shutil.rmtree(pasta)
                print(f"  ✓ Pasta {pasta} removida")
            except Exception as e:
                print(f"  ⚠️ Erro ao remover {pasta}: {e}")
    
    # Remover arquivos .spec
    for arquivo in os.listdir('.'):
        if arquivo.endswith('.spec'):
            try:
                os.remove(arquivo)
                print(f"  ✓ Arquivo {arquivo} removido")
            except:
                pass

def criar_pasta_build():
    """Cria a estrutura de pastas para as builds"""
    print("\n📁 Criando estrutura de pastas...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "dist"), exist_ok=True)
    print(f"  ✓ Estrutura {OUTPUT_DIR}/ e {OUTPUT_DIR}/dist/ criada")

def compilar_organizador():
    """Compila o script organizador FileORZ.py"""
    print("\n📦 Compilando o organizador (FileORZ.py)...")
    
    dist_path = os.path.join(OUTPUT_DIR, "dist")
    
    comando = [
        'pyinstaller',
        '--onedir', 
        '--noconsole',
        '--name=FileORZ',
        '--icon=ui/icon/IconApp.ico',
        f'--distpath={dist_path}',
        '--workpath=build_orz',
        '--clean',
        '--noconfirm',
        'FileORZ.py'
    ]
    
    result = subprocess.run(comando, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  ✅ Organizador compilado em {OUTPUT_DIR}/dist/FileORZ.exe")
    else:
        print(f"  ❌ Erro ao compilar organizador")
        print(result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
        return False
    
    return True

def compilar_ui():
    """Compila a UI principal (index.py com todos os módulos incluídos)"""
    print("\n📦 Compilando a UI (index.py)...")
    
    comando = [
        'pyinstaller',
        '--onedir', 
        '--windowed',
        '--name=FileORZ-UI',
        '--icon=ui/icon/IconApp.ico',
        '--add-data=ui:ui',
        '--add-data=utils:utils',
        '--collect-all=customtkinter',
        '--hidden-import=darkdetect',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=utils.model',
        '--hidden-import=utils.StartTask',
        f'--distpath={OUTPUT_DIR}',
        '--workpath=build_ui',
        '--clean',
        '--noconfirm',
        'ui/index.py'
    ]
    
    result = subprocess.run(comando, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  ✅ UI compilada em {OUTPUT_DIR}/FileORZ-UI.exe")
    else:
        print(f"  ❌ Erro ao compilar UI")
        print(result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
        return False
    
    return True

def copiar_config():
    """Copia o config.json para a pasta do executável da UI"""
    print("\n📋 Copiando config.json...")
    
    config_origem = os.path.join('dist', 'config.json')
    # Com --onedir, a UI fica em FileORZ/FileORZ-UI/
    config_destino_ui = os.path.join(OUTPUT_DIR, 'FileORZ-UI', 'config.json')
    # O organizador também precisa do config em FileORZ/dist/FileORZ/
    config_destino_orz = os.path.join(OUTPUT_DIR, 'dist', 'FileORZ', 'config.json')
    
    if os.path.exists(config_origem):
        # Copiar para pasta da UI
        if os.path.exists(os.path.dirname(config_destino_ui)):
            shutil.copy(config_origem, config_destino_ui)
            print(f"  ✅ config.json copiado para {OUTPUT_DIR}/FileORZ-UI/")
        
        # Copiar para pasta do organizador
        if os.path.exists(os.path.dirname(config_destino_orz)):
            shutil.copy(config_origem, config_destino_orz)
            print(f"  ✅ config.json copiado para {OUTPUT_DIR}/dist/FileORZ/")
    else:
        print(f"  ⚠️ config.json não encontrado em {config_origem}")

def limpar_temporarios():
    """Limpa arquivos temporários do PyInstaller"""
    print("\n🧹 Limpando arquivos temporários...")
    
    pastas = ['build_ui', 'build_orz']
    
    for pasta in pastas:
        if os.path.exists(pasta):
            try:
                shutil.rmtree(pasta)
                print(f"  ✓ Pasta {pasta} removida")
            except:
                pass
    
    # Remover arquivos .spec gerados
    for arquivo in os.listdir('.'):
        if arquivo.endswith('.spec'):
            try:
                os.remove(arquivo)
                print(f"  ✓ Arquivo {arquivo} removido")
            except:
                pass

if __name__ == "__main__":
    print("=" * 50)
    print("🔧 AutoBuild - FileORZ")
    print("=" * 50)
    
    # 1. Limpar builds anteriores
    limpar_builds_anteriores()
    
    # 2. Criar estrutura de pastas
    criar_pasta_build()
    
    # 3. Compilar organizador (FileORZ.py → FileORZ/dist/)
    if not compilar_organizador():
        print("\n❌ Falha na compilação do organizador!")
        exit(1)
    
    # 4. Compilar UI (index.py → FileORZ/)
    if not compilar_ui():
        print("\n❌ Falha na compilação da UI!")
        exit(1)
    
    # 5. Copiar config.json para FileORZ/dist/
    copiar_config()
    
    # 6. Limpar temporários
    limpar_temporarios()
    
    print("\n" + "=" * 50)
    print("✅ Compilação concluída com sucesso!")
    print("=" * 50)
    print(f"\n📁 Estrutura criada:")
    print(f"   {OUTPUT_DIR}/")
    print(f"   ├── FileORZ-UI.exe     (UI Principal)")
    print(f"   └── dist/")
    print(f"       ├── FileORZ.exe    (Organizador)")
    print(f"       └── config.json    (Configurações)")
    print("=" * 50)