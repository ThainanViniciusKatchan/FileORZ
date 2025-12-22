import json
import os
from pathlib import Path
from typing import Dict, List

class FileTypeConfig:
    def __init__(self, config_file: str = "config.json"):
        # Configuração padrão com todos os tipos de arquivo
        self.default_config = {
            "documentos": self._create_default_extensions([
                ".pdf", ".doc", ".txt", ".pptx", ".docx", ".xlsx",
                ".xlsm", ".csv", ".xls", ".dotm", ".ponto", ".dotx",
                ".htm", ".html", ".cfg", ".alg"
            ], default=True),
            
            "videos": self._create_default_extensions([
                ".mov", ".mp4", ".avi", ".av1", ".mpeg-2", ".avchd",
                ".aac", ".mkv", ".divx", ".h.264", ".mpeg-1", ".wmv"
            ], default=True),
            
            "audios": self._create_default_extensions([
                ".mp3", ".wav", ".flac", ".3GP", ".M4A", ".ogg",
                ".wma", ".m4a", ".webm"
            ], default=True),
            
            "compactos": self._create_default_extensions([
                ".rar", ".zip", ".zpix", ".7z", ".rar5", ".iso",
                ".gzip", ".7-zip", ".tar"
            ], default=True),
            
            "fontes": self._create_default_extensions([
                ".ttf", ".eot", ".woff", ".woff2"
            ], default=True),
            
            "setups": self._create_default_extensions([
                ".exe", ".msi", ".appx", ".appxbundle", ".msix", ".apk"
            ], default=True), 
            
            "imagens": self._create_default_extensions([
                ".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif",
                ".cr3", ".cr2", ".exif", ".psd", ".eps", ".ai",
                ".svg", ".webp", ".heic", ".heif", ".raw", ".af"
            ], default=True)
        }
        
        self.config = self.load_config()
    
    def _create_default_extensions(self, extensions: List[str], default: bool = True) -> Dict[str, bool]:
        """Cria dicionário de extensões com valor padrão"""
        return {ext: default for ext in extensions}
    
    def load_config(self) -> Dict[str, Dict[str, bool]]:
        """Carrega configuração do arquivo ou usa padrão"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Mescla configurações, mantendo novas extensões
                    return self._merge_configs(loaded_config)
            except Exception as e:
                print(f"Erro ao carregar configuração: {e}")
                return self.default_config.copy()
        return self.default_config.copy()
    
    def _merge_configs(self, loaded_config: Dict) -> Dict:
        """Mescla configuração carregada com padrão para manter compatibilidade"""
        merged = self.default_config.copy()
        
        for category in merged:
            if category in loaded_config:
                for ext in merged[category]:
                    if ext in loaded_config[category]:
                        merged[category][ext] = loaded_config[category][ext]
        return merged
    
    def save_config(self):
        """Salva configuração atual no arquivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
            return False
    
    def get_category(self, category: str) -> Dict[str, bool]:
        """Obtém todas as extensões de uma categoria"""
        return self.config.get(category, {})
    
    def set_extension(self, category: str, extension: str, enabled: bool):
        """Define o estado de uma extensão específica"""
        if category in self.config and extension in self.config[category]:
            self.config[category][extension] = enabled
            self.save_config()
    
    def toggle_extension(self, category: str, extension: str):
        """Alterna o estado de uma extensão"""
        if category in self.config and extension in self.config[category]:
            self.config[category][extension] = not self.config[category][extension]
            self.save_config()
    
    def get_all_enabled_extensions(self) -> List[str]:
        """Retorna lista de todas as extensões ativadas"""
        enabled = []
        for category in self.config.values():
            for ext, is_enabled in category.items():
                if is_enabled:
                    enabled.append(ext.lower())
        return enabled
    
    def is_extension_enabled(self, extension: str) -> bool:
        """Verifica se uma extensão específica está ativada"""
        ext_lower = extension.lower()
        for category in self.config.values():
            for ext, is_enabled in category.items():
                if ext.lower() == ext_lower:
                    return is_enabled
        return False
    
    def reset_to_default(self):
        """Reseta todas as configurações para o padrão"""
        self.config = self.default_config.copy()
        self.save_config()
    
    def export_config(self, filepath: str):
        """Exporta configuração para outro arquivo"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao exportar configuração: {e}")
            return False