import re
import sys
import argparse
from pathlib import Path

def get_current_version(file_path):
    content = file_path.read_text(encoding='utf-8')
    match = re.search(r'__version__\s*=\s*"([^"]+)"', content)
    if match:
        return match.group(1)
    raise ValueError("Versão não encontrada no arquivo.")

def bump_version(current_version, increment_type):
    # Validar formato SemVer simples (Major.Minor.Patch)
    parts = list(map(int, current_version.split('.')))
    if len(parts) != 3:
        raise ValueError(f"Versão atual '{current_version}' não está no formato Major.Minor.Patch")

    major, minor, patch = parts

    if increment_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif increment_type == 'minor':
        minor += 1
        patch = 0
    elif increment_type == 'patch':
        patch += 1
    elif increment_type == 'none':
        pass # Apenas retornar a versão atual
    
    return f"{major}.{minor}.{patch}"

def update_file(file_path, new_version):
    content = file_path.read_text(encoding='utf-8')
    new_content = re.sub(
        r'__version__\s*=\s*"[^"]+"',
        f'__version__ = "{new_version}"',
        content
    )
    file_path.write_text(new_content, encoding='utf-8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Atualizar versão do projeto.')
    parser.add_argument('increment', choices=['major', 'minor', 'patch', 'none', 'set-version'], help='Tipo de incremento')
    parser.add_argument('--set', help='Valor específico da versão (usado com set-version)')
    
    args = parser.parse_args()
    
    version_file = Path('utils/version.py')
    
    if not version_file.exists():
        print(f"Erro: Arquivo {version_file} não encontrado.", file=sys.stderr)
        sys.exit(1)

    current_version = get_current_version(version_file)
    
    if args.increment == 'set-version':
        if not args.set:
             print("Erro: --set é obrigatório para set-version", file=sys.stderr)
             sys.exit(1)
        new_version = args.set
    else:
        new_version = bump_version(current_version, args.increment)
    
    if args.increment != 'none':
        update_file(version_file, new_version)
        print(f"Versão atualizada: {current_version} -> {new_version}", file=sys.stderr)
    
    # Imprimir apenas a nova versão para o stdout (pode ser capturado pelo Actions)
    print(new_version)
