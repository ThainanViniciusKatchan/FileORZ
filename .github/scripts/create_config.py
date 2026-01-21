import json
import os

def create_default_config():
    config = {
        "documentos": {
        ".pdf": true,
        ".doc": true,
        ".txt": true,
        ".pptx": true,
        ".docx": true,
        ".xlsx": true,
        ".xlsm": true,
        ".csv": true,
        ".xls": true,
        ".dotm": true,
        ".ponto": true,
        ".dotx": true,
        ".htm": true,
        ".html": true,
        ".cfg": true,
        ".alg": true,
        ".md": true,
        ".ftl": true
    },
    "videos": {
        ".mov": true,
        ".mp4": true,
        ".avi": true,
        ".av1": true,
        ".mpeg-2": true,
        ".avchd": true,
        ".aac": true,
        ".mkv": true,
        ".divx": true,
        ".h.264": true,
        ".mpeg-1": true,
        ".wmv": true
    },
    "audios": {
        ".mp3": true,
        ".wav": true,
        ".flac": true,
        ".3GP": true,
        ".M4A": true,
        ".ogg": true,
        ".wma": true,
        ".m4a": true,
        ".webm": true
    },
    "compactos": {
        ".rar": true,
        ".zip": true,
        ".zpix": true,
        ".7z": true,
        ".rar5": true,
        ".iso": true,
        ".gzip": true,
        ".7-zip": true,
        ".tar": true
    },
    "fontes": {
        ".ttf": true,
        ".eot": true,
        ".woff": true,
        ".woff2": true
    },
    "setups": {
        ".exe": true,
        ".msi": true,
        ".appx": true,
        ".appxbundle": true,
        ".msix": true,
        ".apk": true,
        ".Msixbundle": true
    },
    "imagens": {
        ".jpg": true,
        ".jpeg": true,
        ".png": true,
        ".bmp": true,
        ".tiff": true,
        ".gif": true,
        ".cr3": true,
        ".cr2": true,
        ".exif": true,
        ".psd": true,
        ".eps": true,
        ".ai": true,
        ".svg": true,
        ".webp": true,
        ".heic": true,
        ".heif": true,
        ".raw": true,
        ".af": true
    },
    "timeverification": "5",
    "Startup": False,
    "Folder": "pasta de organização"
    }
    
    config_path = os.path.join(os.getcwd(), 'config.json')
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    print(f"config.json padrão criado em: {config_path}")

if __name__ == "__main__":
    create_default_config()
