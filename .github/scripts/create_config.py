import json
import os

def create_default_config():
    config = {
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
        ".eps": True,
        ".ai": True,
        ".svg": True,
        ".webp": True,
        ".heic": True,
        ".heif": True,
        ".raw": True,
        ".af": True
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
